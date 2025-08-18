"""PR review orchestrator using local Git + YunXiao API + Claude Code SDK."""

import os
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
import asyncio
from loguru import logger

from ..integrations.ali_yunxiao import AliYunXiaoClient
from ..integrations.git_handler import GitHandler
from ..integrations.claude_code_runner import ClaudeCodeRunner
from .prompt_reader import PromptReader


class PRReviewer:
    """PR review orchestrator that coordinates Git, YunXiao API, and Claude Code SDK."""

    def __init__(self, prompts_dir: Optional[Path] = None):
        """Initialize PR reviewer with necessary clients."""
        logger.info("Initializing PR reviewer")

        try:
            self.yunxiao_client = AliYunXiaoClient()
            logger.info("Ali YunXiao client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Ali YunXiao client: {e}")
            raise

        try:
            self.git_handler = GitHandler()
            logger.info("Git handler initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Git handler: {e}")
            raise

        try:
            self.claude_runner = ClaudeCodeRunner(max_turns=5)
            logger.info("Claude Code runner initialized successfully with max_turns=5")
        except Exception as e:
            logger.error(f"Failed to initialize Claude Code runner: {e}")
            raise

        # Initialize prompt reader
        if prompts_dir is None:
            # Default to config/system_prompts relative to project root
            project_root = Path(__file__).parent.parent.parent.parent
            prompts_dir = project_root / "config" / "system_prompts"

        try:
            self.prompt_reader = PromptReader(prompts_dir)
            logger.info(f"Prompt reader initialized with directory: {prompts_dir}")
        except Exception as e:
            logger.error(f"Failed to initialize prompt reader: {e}")
            raise

        # Get current branch from environment or Git
        try:
            self.current_branch = self.git_handler.get_current_branch_from_env()
            logger.info(f"Current branch detected from environment: {self.current_branch}")
        except ValueError:
            # Fallback to git if CI environment is not available
            logger.warning("CI environment not available, falling back to Git command")
            try:
                self.current_branch = self.git_handler.get_current_branch()
                logger.info(f"Current branch detected from Git: {self.current_branch}")
            except Exception as e:
                logger.error(f"Failed to get current branch: {e}")
                raise

        # Track phase comments for updates
        self.phase_comment_ids: Dict[str, str] = {}
        # Track phase start times for duration calculation
        self.phase_start_times: Dict[str, float] = {}

    async def review_current_pr(self, target_branch: str = 'master') -> Dict[str, Any]:
        """Review the current branch's PR against target branch using phased approach."""
        logger.info(f"Starting PR review for current branch: {self.current_branch} -> {target_branch}")

        try:
            # Find the PR for current branch
            logger.debug(f"Searching for PR: {self.current_branch} -> {target_branch}")
            pr = self.yunxiao_client.find_pull_request_by_branch(
                source_branch=self.current_branch,
                target_branch=target_branch
            )

            if not pr:
                logger.error(f"No open PR found for branch {self.current_branch} -> {target_branch}")
                raise ValueError(f"No open PR found for branch {self.current_branch} -> {target_branch}")

            logger.info(f"Found PR #{pr.get('localId')}: {pr.get('title', 'Unknown title')}")
            return await self._execute_phased_review(pr, target_branch)

        except Exception as e:
            logger.error(f"Failed to review current PR: {e}")
            raise

    async def review_specific_pr(self, pr_local_id: int) -> Dict[str, Any]:
        """Review a specific PR by its local ID using phased approach."""
        logger.info(f"Starting review for specific PR #{pr_local_id}")

        try:
            # Get PR details from YunXiao
            logger.debug(f"Fetching PR details for ID: {pr_local_id}")
            prs = self.yunxiao_client.get_pull_requests(state='opened')
            pr = next((p for p in prs if p['localId'] == pr_local_id), None)

            if not pr:
                logger.error(f"PR with local ID {pr_local_id} not found")
                raise ValueError(f"PR with local ID {pr_local_id} not found")

            logger.info(f"Found PR #{pr_local_id}: {pr.get('title', 'Unknown title')} ({pr.get('sourceBranch')} -> {pr.get('targetBranch')})")
            return await self._execute_phased_review(pr, pr.get('targetBranch', 'master'))

        except Exception as e:
            logger.error(f"Failed to review specific PR #{pr_local_id}: {e}")
            raise

    async def _execute_phased_review(self, pr: Dict[str, Any], target_branch: str) -> Dict[str, Any]:
        """Execute the three-phase review process with progress comments."""
        pr_local_id = pr['localId']
        source_branch = pr.get('sourceBranch', self.current_branch)

        logger.info(f"Executing phased review for PR #{pr_local_id}: {source_branch} -> {target_branch}")
        
        # Reset phase comment tracking for this PR
        self.phase_comment_ids.clear()
        self.phase_start_times.clear()

        # Get diff content
        logger.debug(f"Getting diff content between {target_branch} and {source_branch}")
        diff_content = self._get_branch_diff(target_branch, source_branch)

        if not diff_content.strip():
            logger.warning(f"No changes detected between {target_branch} and {source_branch}")
            return {
                'status': 'no_changes',
                'message': 'No changes detected between branches',
                'pr_id': pr_local_id
            }

        logger.info(f"Diff content retrieved, size: {len(diff_content)} characters")

        # Get patch set IDs for comments
        to_patch_set_id = pr.get('toPatchSetId', '')
        logger.debug(f"Using patch set ID: {to_patch_set_id}")

        try:
            # Phase 1: Summary Generation
            logger.info("Starting Phase 1: Summary Generation")
            await self._post_phase_start_comment(pr_local_id, "Summary Generation", to_patch_set_id)
            summary_result = await self._phase_1_summary(pr, diff_content)
            logger.info(f"Phase 1 completed, summary length: {len(summary_result)} characters")
            await self._post_phase_result_comment(pr_local_id, "Summary Generation", summary_result, to_patch_set_id)

            # Phase 2: Change Analysis
            logger.info("Starting Phase 2: Change Analysis")
            await self._post_phase_start_comment(pr_local_id, "Change Analysis", to_patch_set_id)
            analysis_result = await self._phase_2_analysis(pr, diff_content, summary_result)
            logger.info(f"Phase 2 completed, analysis length: {len(analysis_result)} characters")
            await self._post_phase_result_comment(pr_local_id, "Change Analysis", analysis_result, to_patch_set_id)

            # Phase 3: Comment Generation
            logger.info("Starting Phase 3: Comment Generation")
            await self._post_phase_start_comment(pr_local_id, "Comment Generation", to_patch_set_id)
            comments_result = await self._phase_3_comments(pr, diff_content, analysis_result)
            logger.info(f"Phase 3 completed, generated {len(comments_result)} comments")
            
            # Update comment generation phase with summary before posting inline comments
            await self._post_phase_result_comment(pr_local_id, "Comment Generation", 
                f"Generated {len(comments_result)} inline comments. Posting them now...", to_patch_set_id)
            
            # Post inline comments
            await self._post_inline_comments(pr, comments_result)
            
            # Final update after all inline comments are posted
            await self._update_comment_generation_final(pr_local_id, len(comments_result))

            # Final summary comment
            logger.info("Posting final summary comment")
            await self._post_final_summary(pr, summary_result, analysis_result, comments_result)

            result = {
                'status': 'completed',
                'pr_id': pr_local_id,
                'pr_title': pr['title'],
                'summary': summary_result,
                'analysis': analysis_result,
                'comments_posted': len(comments_result),
                'comments': comments_result
            }

            logger.success(f"PR review completed successfully for #{pr_local_id}")
            return result

        except Exception as e:
            logger.error(f"Error during phased review execution: {e}")
            # Post error comment
            await self._post_error_comment(pr_local_id, str(e), to_patch_set_id)
            raise

    async def _phase_1_summary(self, pr: Dict[str, Any], diff_content: str) -> str:
        """Phase 1: Generate PR summary using system prompt."""
        logger.debug("Phase 1: Reading summary system prompt")
        system_prompt = self.prompt_reader.read_system_prompt('summary')

        context = {
            'pr_title': pr.get('title', 'Unknown'),
            'pr_description': pr.get('description', 'No description'),
            'source_branch': pr.get('sourceBranch', 'unknown'),
            'target_branch': pr.get('targetBranch', 'unknown'),
            'diff_content': diff_content
        }

        logger.debug(f"Phase 1: Building prompt for PR: {context['pr_title']}")
        prompt = f"""Please generate a summary for this Pull Request:

PR Title: {context['pr_title']}
PR Description: {context['pr_description']}
Source Branch: {context['source_branch']}
Target Branch: {context['target_branch']}

Git Diff:
{diff_content}

Please provide a comprehensive summary following the system prompt guidelines."""

        logger.debug("Phase 1: Sending request to Claude Code SDK")
        try:
            result = await self.claude_runner.run_async(system_prompt, prompt)
            logger.debug(f"Phase 1: Received response from Claude, length: {len(result)} characters")
            return result
        except Exception as e:
            logger.error(f"Phase 1: Claude Code SDK request failed: {e}")
            raise

    async def _phase_2_analysis(self, pr: Dict[str, Any], diff_content: str, summary: str) -> str:
        """Phase 2: Analyze changes using system prompt."""
        logger.debug("Phase 2: Reading analysis system prompt")
        system_prompt = self.prompt_reader.read_system_prompt('analysis')

        logger.debug(f"Phase 2: Building analysis prompt for PR: {pr.get('title', 'Unknown')}")
        prompt = f"""Please analyze this Pull Request based on the previous summary:

Previous Summary:
{summary}

PR Details:
- Title: {pr.get('title', 'Unknown')}
- Description: {pr.get('description', 'No description')}
- Source Branch: {pr.get('sourceBranch', 'unknown')}
- Target Branch: {pr.get('targetBranch', 'unknown')}

Git Diff:
{diff_content}

Please provide a detailed technical analysis following the system prompt guidelines."""

        logger.debug("Phase 2: Sending analysis request to Claude Code SDK")
        try:
            result = await self.claude_runner.run_async(system_prompt, prompt)
            logger.debug(f"Phase 2: Received analysis response from Claude, length: {len(result)} characters")
            return result
        except Exception as e:
            logger.error(f"Phase 2: Claude Code SDK analysis request failed: {e}")
            raise

    async def _phase_3_comments(self, pr: Dict[str, Any], diff_content: str, analysis: str) -> List[Dict[str, Any]]:
        """Phase 3: Generate specific comments using system prompt."""
        logger.debug("Phase 3: Reading comment system prompt")
        system_prompt = self.prompt_reader.read_system_prompt('comment')

        logger.debug(f"Phase 3: Building comment generation prompt for PR: {pr.get('title', 'Unknown')}")
        prompt = f"""Please generate specific comments for this Pull Request based on the previous analysis:

Previous Analysis:
{analysis}

PR Details:
- Title: {pr.get('title', 'Unknown')}
- Description: {pr.get('description', 'No description')}

Git Diff:
{diff_content}

Please provide specific, actionable comments following the system prompt guidelines."""

        logger.debug("Phase 3: Sending comment generation request to Claude Code SDK")
        try:
            response = await self.claude_runner.run_async(system_prompt, prompt, max_turns=10)
            logger.debug(f"Phase 3: Received comment response from Claude, length: {len(response)} characters")

            logger.debug("Phase 3: Parsing comment response")
            comments = self._parse_comment_response(response)
            logger.debug(f"Phase 3: Parsed {len(comments)} comments from response")
            return comments
        except Exception as e:
            logger.error(f"Phase 3: Claude Code SDK comment generation failed: {e}")
            raise

    async def _post_phase_start_comment(self, pr_local_id: int, phase_name: str, patch_set_id: str):
        """Post a comment indicating the start of a review phase."""
        logger.debug(f"Posting phase start comment for {phase_name} on PR #{pr_local_id}")
        try:
            # Record start time
            self.phase_start_times[phase_name.lower()] = time.time()
            
            result = self.yunxiao_client.create_global_comment(
                pr_local_id,
                f"🔄 **Review Phase Started**: {phase_name}\n\n_Processing..._",
                patch_set_id
            )
            # Store comment ID for later update
            comment_biz_id = result.get('comment_biz_id')
            if comment_biz_id:
                self.phase_comment_ids[phase_name.lower()] = comment_biz_id
                logger.debug(f"Stored comment ID {comment_biz_id} for phase {phase_name}")
            
            logger.debug(f"Successfully posted phase start comment for {phase_name}")
        except Exception as e:
            logger.error(f"Failed to post phase start comment for {phase_name}: {e}")

    async def _post_phase_result_comment(self, pr_local_id: int, phase_name: str, result: str, patch_set_id: str):
        """Update the phase comment with the result."""
        logger.debug(f"Updating phase result comment for {phase_name} on PR #{pr_local_id}")
        try:
            phase_key = phase_name.lower()
            comment_biz_id = self.phase_comment_ids.get(phase_key)
            
            # Calculate elapsed time
            start_time = self.phase_start_times.get(phase_key)
            elapsed_str = ""
            if start_time:
                elapsed = time.time() - start_time
                elapsed_str = f" _(completed in {elapsed:.1f}s)_"
            
            if comment_biz_id:
                # Update existing comment
                logger.debug(f"Updating existing comment {comment_biz_id} for phase {phase_name}")
                self.yunxiao_client.update_pr_comment(
                    pr_local_id,
                    comment_biz_id,
                    content=f"✅ **{phase_name} Complete**{elapsed_str}\n\n{result}"
                )
                logger.debug(f"Successfully updated phase result comment for {phase_name}")
            else:
                # Fallback to creating new comment if ID not found
                logger.warning(f"No stored comment ID for phase {phase_name}, creating new comment")
                self.yunxiao_client.create_global_comment(
                    pr_local_id,
                    f"✅ **{phase_name} Complete**{elapsed_str}\n\n{result}",
                    patch_set_id
                )
                logger.debug(f"Successfully created fallback phase result comment for {phase_name}")
        except Exception as e:
            logger.error(f"Failed to update/post phase result comment for {phase_name}: {e}")

    async def _post_inline_comments(self, pr: Dict[str, Any], comments: List[Dict[str, Any]]):
        """Post inline comments to specific lines with progress updates."""
        pr_local_id = pr['localId']
        from_patch_set_id = pr.get('fromPatchSetId', '')
        to_patch_set_id = pr.get('toPatchSetId', '')

        logger.info(f"Posting {len(comments)} inline comments to PR #{pr_local_id}")

        for i, comment in enumerate(comments, 1):
            # Update progress every 5 comments or on last comment
            if i % 5 == 0 or i == len(comments):
                progress_msg = f"Posting inline comments: {i}/{len(comments)} completed"
                await self._update_phase_progress(pr_local_id, "Comment Generation", progress_msg)
            
            if comment.get('file') and comment.get('line'):
                logger.debug(f"Posting inline comment {i}/{len(comments)}: {comment['file']}:{comment['line']}")
                try:
                    self.yunxiao_client.create_inline_comment(
                        pr_local_id,
                        f"**{comment.get('type', 'COMMENT')}**: {comment['content']}",
                        comment['file'],
                        int(comment['line']),
                        from_patch_set_id,
                        to_patch_set_id
                    )
                    logger.debug(f"Successfully posted inline comment {i}/{len(comments)}")
                except Exception as e:
                    logger.error(f"Failed to post inline comment for {comment['file']}:{comment['line']}: {e}")
            else:
                logger.warning(f"Skipping comment {i}/{len(comments)} - missing file or line information: {comment}")

    async def _post_final_summary(self, pr: Dict[str, Any], summary: str, analysis: str, comments: List[Dict[str, Any]]):
        """Post final review summary."""
        pr_local_id = pr['localId']
        to_patch_set_id = pr.get('toPatchSetId', '')

        final_summary = f"""🎯 **Code Review Complete**

**Summary**: {len(summary.split())} words
**Analysis**: {len(analysis.split())} words
**Comments Generated**: {len(comments)}

The automated review has been completed. Please review all comments and address any issues marked as MUST_FIX or SHOULD_FIX."""

        logger.info(f"Posting final summary for PR #{pr_local_id}")
        try:
            self.yunxiao_client.create_global_comment(
                pr_local_id,
                final_summary,
                to_patch_set_id
            )
            logger.info(f"Successfully posted final summary for PR #{pr_local_id}")
        except Exception as e:
            logger.error(f"Failed to post final summary: {e}")

    async def _post_error_comment(self, pr_local_id: int, error_message: str, patch_set_id: str):
        """Post an error comment if review fails."""
        logger.warning(f"Posting error comment for PR #{pr_local_id}: {error_message}")
        try:
            self.yunxiao_client.create_global_comment(
                pr_local_id,
                f"❌ **Review Error**: {error_message}",
                patch_set_id
            )
            logger.info(f"Successfully posted error comment for PR #{pr_local_id}")
        except Exception as e:
            logger.error(f"Failed to post error comment: {e}")

    def _get_branch_diff(self, base_branch: str, compare_branch: str) -> str:
        """Get diff between two branches using GitHandler."""
        logger.debug(f"Getting branch diff: {base_branch}..{compare_branch}")
        try:
            diff = self.git_handler.get_branch_diff(base_branch, compare_branch)
            logger.debug(f"Retrieved diff, size: {len(diff)} characters")
            return diff
        except Exception as e:
            logger.error(f"Failed to get branch diff: {e}")
            raise

    def _parse_comment_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse Claude's comment response into structured comment data."""
        logger.debug(f"Parsing comment response, length: {len(response)} characters")
        comments = []
        lines = response.split('\n')
        current_comment = {}

        for line in lines:
            line = line.strip()

            if line.startswith('File:'):
                if current_comment:  # Save previous comment
                    comments.append(current_comment)
                current_comment = {'file': line.split(':', 1)[1].strip()}
            elif line.startswith('Line:'):
                current_comment['line'] = line.split(':', 1)[1].strip()
            elif line.startswith('Type:'):
                current_comment['type'] = line.split(':', 1)[1].strip()
            elif line.startswith('Comment:'):
                current_comment['content'] = line.split(':', 1)[1].strip()

        # Add the last comment
        if current_comment:
            comments.append(current_comment)

        logger.debug(f"Parsed {len(comments)} comments from response")
        return comments

    async def _update_comment_generation_final(self, pr_local_id: int, comment_count: int):
        """Final update to comment generation phase after inline comments are posted."""
        try:
            phase_key = "comment generation"
            comment_biz_id = self.phase_comment_ids.get(phase_key)
            
            # Calculate elapsed time  
            start_time = self.phase_start_times.get(phase_key)
            elapsed_str = ""
            if start_time:
                elapsed = time.time() - start_time
                elapsed_str = f" _(completed in {elapsed:.1f}s)_"
            
            if comment_biz_id:
                logger.debug(f"Final update to comment generation phase: {comment_count} comments posted")
                self.yunxiao_client.update_pr_comment(
                    pr_local_id,
                    comment_biz_id,
                    content=f"✅ **Comment Generation Complete**{elapsed_str}\\n\\n" +
                           f"Successfully posted {comment_count} inline comments. " +
                           f"Please review all comments and address any issues marked as MUST_FIX or SHOULD_FIX."
                )
                logger.debug("Successfully updated final comment generation status")
        except Exception as e:
            logger.error(f"Failed to update final comment generation status: {e}")

    async def _update_phase_progress(self, pr_local_id: int, phase_name: str, progress_message: str):
        """Update phase comment with intermediate progress message."""
        try:
            phase_key = phase_name.lower()
            comment_biz_id = self.phase_comment_ids.get(phase_key)
            
            # Calculate elapsed time so far
            start_time = self.phase_start_times.get(phase_key)
            elapsed_str = ""
            if start_time:
                elapsed = time.time() - start_time
                elapsed_str = f" _(running {elapsed:.1f}s)_"
            
            if comment_biz_id:
                logger.debug(f"Updating progress for {phase_name}: {progress_message}")
                self.yunxiao_client.update_pr_comment(
                    pr_local_id,
                    comment_biz_id,
                    content=f"🔄 **{phase_name} In Progress**{elapsed_str}\\n\\n{progress_message}"
                )
        except Exception as e:
            logger.error(f"Failed to update phase progress for {phase_name}: {e}")