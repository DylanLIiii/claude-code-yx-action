"""PR review orchestrator using local Git + YunXiao API + Claude Code SDK."""

import os
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from loguru import logger

from ..integrations.ali_yunxiao import AliYunXiaoClient
from ..integrations.git_handler import GitHandler
from ..integrations.claude_code_runner import ClaudeCodeRunner
from ..integrations.openai_runner import OpenAIRunner
from .prompt_reader import PromptReader
from .utils import JsonDumper, split_thinking_and_json, safe_json_repair
from .output_formatter import OutputFormatter
# from json_repair import repair_json  # Now using safe_json_repair instead


class PRReviewer:
    """PR review orchestrator that coordinates Git, YunXiao API, and Claude Code SDK."""

    def __init__(self, prompts_dir: Optional[Path] = None, modes: Optional[List[str]] = None):
        """Initialize PR reviewer with necessary clients.

        Args:
            prompts_dir: Directory containing system prompts
            modes: List of review modes to enable ['summary', 'analysis', 'comments']
        """
        logger.info("Initializing PR reviewer")

        # Set default modes if none provided
        self.enabled_modes = modes or ['summary', 'analysis', 'comments']
        logger.info(f"Enabled review modes: {self.enabled_modes}")

        try:
            self.yunxiao_client = AliYunXiaoClient()
            logger.info("Ali YunXiao client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Ali YunXiao client: {e}")
            raise

        try:
            self.claude_runner = OpenAIRunner(max_turns=5)
            logger.info("Claude Code runner initialized successfully with max_turns=5")
        except Exception as e:
            logger.error(f"Failed to initialize Claude Code runner: {e}")
            raise

        # Initialize prompt reader
        if prompts_dir is None:
            # Try to find config files in multiple locations:
            # 1. Development: config/system_prompts relative to project root
            # 2. Installed: yx_cc/config/system_prompts relative to package installation

            # First try development path (relative to project root)
            project_root = Path(__file__).parent.parent.parent.parent
            dev_prompts_dir = project_root / "config" / "system_prompts"

            # Then try installed path (within package)
            package_dir = Path(__file__).parent.parent
            installed_prompts_dir = package_dir / "config" / "system_prompts"

            if dev_prompts_dir.exists():
                prompts_dir = dev_prompts_dir
            elif installed_prompts_dir.exists():
                prompts_dir = installed_prompts_dir
            else:
                # Fallback to development path for error reporting
                prompts_dir = dev_prompts_dir

        try:
            self.prompt_reader = PromptReader(prompts_dir)
            logger.info(f"Prompt reader initialized with directory: {prompts_dir}")
        except Exception as e:
            logger.error(f"Failed to initialize prompt reader: {e}")
            raise

        # Initialize git handler (optional)
        self.git_handler = None
        try:
            self.git_handler = GitHandler()
            logger.info("Git handler initialized successfully")
        except Exception as e:
            logger.warning(f"Git handler initialization failed: {e}")

        # Configuration flags
        self.use_yunxiao_for_diff = True

        # Initialize JSON dumper for storing results
        self.json_dumper = JsonDumper()
        logger.info("JSON dumper initialized for storing review results")

        # Initialize output formatter for formatting summary results
        self.output_formatter = OutputFormatter(format_type='markdown')
        logger.info("Output formatter initialized for markdown formatting")

        # Get current branch - prioritize environment variables, fallback to git if available
        self.current_branch = self._get_current_branch()

        # Track phase comments for updates
        self.phase_comment_ids: Dict[str, str] = {}
        # Track phase start times for duration calculation
        self.phase_start_times: Dict[str, float] = {}

        # Cache for PR context to avoid repeated API calls
        self._pr_context_cache: Dict[str, Any] = {}

    def _get_last_reviewed_patch_set(self, pr_local_id: int) -> Optional[str]:
        """Get the last reviewed patch set ID from existing comments.

        Args:
            pr_local_id: The local ID of the pull request.

        Returns:
            The patch set ID of the last review, or None if no previous review found.
        """
        logger.debug(f"Looking for last reviewed patch set for PR #{pr_local_id}")
        try:
            comments = self.yunxiao_client.list_merge_request_comments(pr_local_id)

            last_version = -1
            last_patch_set_id = None

            for comment in comments:
                # Check for our tool's comments
                if "related_patchset" in comment and comment["related_patchset"]:
                    patch_set = comment["related_patchset"]
                    version_no = patch_set.get("versionNo")
                    patch_set_id = patch_set.get("patchSetBizId")

                    if version_no is not None and patch_set_id:
                        if version_no > last_version:
                            last_version = version_no
                            last_patch_set_id = patch_set_id

            if last_patch_set_id:
                logger.info(f"Found last reviewed patch set for PR #{pr_local_id}: {last_patch_set_id} (version {last_version})")
            else:
                logger.info(f"No previously reviewed patch set found for PR #{pr_local_id}")

            return last_patch_set_id

        except Exception as e:
            logger.warning(f"Could not determine last reviewed patch set for PR #{pr_local_id}: {e}")
            return None

    def get_existing_phase_context(self, pr_local_id: int, phase_name: str) -> Optional[str]:
        """Retrieve existing phase results from PR comments using ListMergeRequestComments API.

        Args:
            pr_local_id: PR local ID
            phase_name: Phase name to look for ('Summary Generation', 'Change Analysis', 'Comment Generation')

        Returns:
            Existing phase result content or None if not found
        """
        try:
            logger.debug(f"Retrieving existing context for phase '{phase_name}' from PR #{pr_local_id}")

            # Get all comments for the PR
            comments = self.yunxiao_client.list_merge_request_comments(
                pr_local_id,
                comment_type="GLOBAL_COMMENT"
            )

            # Look for phase completion comments
            phase_marker = f"**{phase_name} Complete**"
            for comment in comments:
                content = comment.get('content', '')
                if phase_marker in content:
                    # Extract the content after the phase marker
                    lines = content.split('\n')
                    result_lines = []
                    found_marker = False

                    for line in lines:
                        if phase_marker in line:
                            found_marker = True
                            continue
                        if found_marker and line.strip():
                            result_lines.append(line)

                    if result_lines:
                        result = '\n'.join(result_lines).strip()
                        logger.info(f"Found existing {phase_name} context: {len(result)} characters")
                        return result

            logger.debug(f"No existing context found for phase '{phase_name}'")
            return None

        except Exception as e:
            logger.warning(f"Failed to retrieve existing context for phase '{phase_name}': {e}")
            return None

    async def run_summary_phase(self, pr: Dict[str, Any], diff_content: str,
                               force_regenerate: bool = False) -> str:
        """Run only the summary generation phase.

        Args:
            pr: PR information
            diff_content: Git diff content
            force_regenerate: Whether to regenerate even if existing summary found

        Returns:
            Summary result
        """
        if 'summary' not in self.enabled_modes:
            logger.info("Summary phase disabled, skipping")
            return ""

        pr_local_id = pr['localId']

        # Check for existing summary unless forced to regenerate
        if not force_regenerate:
            existing_summary = self.get_existing_phase_context(pr_local_id, "Summary Generation")
            if existing_summary:
                logger.info("Using existing summary from PR comments")
                return existing_summary

        logger.info("Starting Summary Generation phase")

        # NOTE: Comment posting for summary phase is disabled as per user request.
        # The following lines were removed:
        # await self._post_phase_start_comment(...)
        # await self._post_phase_result_comment(...)

        _, summary_result = await self._phase_1_summary(pr, diff_content)

        # Update PR description with the generated summary
        logger.info("Updating PR description with generated summary")
        await self._update_pr_description(pr_local_id, pr.get('title', 'Unknown'), summary_result)

        return summary_result

    async def run_analysis_phase(self, pr: Dict[str, Any], diff_content: str,
                                summary_context: Optional[str] = None,
                                force_regenerate: bool = False) -> str:
        """Run only the analysis phase.

        Args:
            pr: PR information
            diff_content: Git diff content
            summary_context: Summary context (will be retrieved if not provided)
            force_regenerate: Whether to regenerate even if existing analysis found

        Returns:
            Analysis result
        """
        if 'analysis' not in self.enabled_modes:
            logger.info("Analysis phase disabled, skipping")
            return ""

        pr_local_id = pr['localId']

        # Check for existing analysis unless forced to regenerate
        if not force_regenerate:
            existing_analysis = self.get_existing_phase_context(pr_local_id, "Change Analysis")
            if existing_analysis:
                logger.info("Using existing analysis from PR comments")
                return existing_analysis

        # Get summary context if not provided
        if summary_context is None:
            summary_context = self.get_existing_phase_context(pr_local_id, "Summary Generation")
            if not summary_context:
                logger.warning("No summary context available for analysis phase")
                summary_context = "No summary available"

        logger.info("Starting Change Analysis phase")
        to_patch_set_id = pr.get('toPatchSetId', '')

        await self._post_phase_start_comment(pr_local_id, "Change Analysis", to_patch_set_id)
        analysis_thinking, analysis_result = await self._phase_2_analysis(pr, diff_content, summary_context)
        await self._post_phase_result_comment(pr_local_id, "Change Analysis", analysis_result, to_patch_set_id, analysis_thinking)

        return analysis_result

    async def run_comments_phase(self, pr: Dict[str, Any], diff_content: str,
                                analysis_context: Optional[str] = None,
                                force_regenerate: bool = False) -> tuple[str, List[Dict[str, Any]]]:
        """Run only the comments generation phase.

        Args:
            pr: PR information
            diff_content: Git diff content
            analysis_context: Analysis context (will be retrieved if not provided)
            force_regenerate: Whether to regenerate even if existing comments found

        Returns:
            Tuple of (raw_result, parsed_comments)
        """
        if 'comments' not in self.enabled_modes:
            logger.info("Comments phase disabled, skipping")
            return "", []

        pr_local_id = pr['localId']

        # Check for existing comments unless forced to regenerate
        if not force_regenerate:
            existing_comments = self.get_existing_phase_context(pr_local_id, "Comment Generation")
            if existing_comments:
                logger.info("Using existing comments from PR comments")
                # Parse the existing comments
                parsed_comments = self._parse_comment_response(existing_comments)
                return existing_comments, parsed_comments

        # Get analysis context if not provided
        if analysis_context is None:
            analysis_context = self.get_existing_phase_context(pr_local_id, "Change Analysis")
            if not analysis_context:
                logger.warning("No analysis context available for comments phase")
                analysis_context = "No analysis available"

        logger.info("Starting Comment Generation phase")
        to_patch_set_id = pr.get('toPatchSetId', '')

        await self._post_phase_start_comment(pr_local_id, "Comment Generation", to_patch_set_id)
        comments_thinking, comments_raw_result, comments_parsed = await self._phase_3_comments(pr, diff_content, analysis_context)
        await self._post_phase_result_comment(pr_local_id, "Comment Generation", comments_raw_result, to_patch_set_id, comments_thinking)

        # Post inline comments
        await self._post_inline_comments(pr, comments_parsed)

        # Final update after all inline comments are posted
        await self._update_comment_generation_final(pr_local_id, len(comments_parsed))

        return comments_raw_result, comments_parsed

    async def run_selective_review(self, pr: Dict[str, Any], target_branch: str,
                                  force_regenerate: bool = False) -> Dict[str, Any]:
        """Run review with only the enabled phases.

        Args:
            pr: PR information
            target_branch: Target branch name
            force_regenerate: Whether to regenerate phases even if existing results found

        Returns:
            Review results
        """
        pr_local_id = pr['localId']
        source_branch = pr.get('sourceBranch', self.current_branch)

        logger.info(f"Running selective review for PR #{pr_local_id}: {source_branch} -> {target_branch}")
        logger.info(f"Enabled phases: {self.enabled_modes}")

        # Reset phase comment tracking for this PR
        self.phase_comment_ids.clear()
        self.phase_start_times.clear()

        # Check for incremental update
        last_reviewed_patch_set_id = self._get_last_reviewed_patch_set(pr_local_id)
        current_patch_set_id = pr.get('toPatchSetId')

        is_incremental_update = last_reviewed_patch_set_id and (last_reviewed_patch_set_id != current_patch_set_id)

        if is_incremental_update:
            logger.info(f"Incremental update detected for PR #{pr_local_id}. Reviewing changes since patch set {last_reviewed_patch_set_id}.")
            # For incremental updates, get diff between patch sets
            diff_content = self._get_diff_content(pr, target_branch, source_branch, from_patch_set_id=last_reviewed_patch_set_id)
            # Disable summary for incremental updates
            enabled_modes = [mode for mode in self.enabled_modes if mode != 'summary']
            logger.info(f"Summary phase disabled for incremental update. Effective modes: {enabled_modes}")
        else:
            logger.info(f"New PR or no previous review found for PR #{pr_local_id}. Performing full review.")
            # Get diff content for the whole PR
            diff_content = self._get_diff_content(pr, target_branch, source_branch)
            enabled_modes = self.enabled_modes

        if not diff_content.strip():
            logger.warning(f"No changes detected between {target_branch} and {source_branch}")
            return {
                'status': 'no_changes',
                'message': 'No changes detected between branches',
                'pr_id': pr_local_id
            }

        logger.info(f"Diff content retrieved, size: {len(diff_content)} characters")

        # Initialize results
        result = {
            'status': 'completed',
            'pr_id': pr_local_id,
            'pr_title': pr['title'],
            'enabled_phases': enabled_modes,
            'summary': '',
            'analysis': '',
            'comments_posted': 0,
            'comments': []
        }

        try:
            # Run enabled phases
            if 'summary' in enabled_modes:
                result['summary'] = await self.run_summary_phase(pr, diff_content, force_regenerate)

            if 'analysis' in enabled_modes:
                result['analysis'] = await self.run_analysis_phase(pr, diff_content, result['summary'], force_regenerate)

            if 'comments' in enabled_modes:
                comments_raw, comments_parsed = await self.run_comments_phase(pr, diff_content, result['analysis'], force_regenerate)
                result['comments_posted'] = len(comments_parsed)
                result['comments'] = comments_parsed
                result['comments_raw'] = comments_raw

            # Post final summary if any phases were run and it's not an incremental update
            if enabled_modes and not is_incremental_update:
                logger.info("Posting final summary comment")
                await self._post_final_summary(pr, result['summary'], result['analysis'], result['comments'])

            # Dump review results to JSON file
            try:
                json_file_path = self.json_dumper.dump_results(f"pr_review_{pr_local_id}", result)
                logger.info(f"PR review results dumped to: {json_file_path}")
            except Exception as e:
                logger.error(f"Failed to dump PR review results to JSON: {e}")

            logger.success(f"Selective PR review completed successfully for #{pr_local_id}")
            return result

        except Exception as e:
            logger.error(f"Error during selective review execution: {e}")
            # Post error comment
            to_patch_set_id = pr.get('toPatchSetId', '')
            await self._post_error_comment(pr_local_id, str(e), to_patch_set_id)
            raise

    def _get_current_branch(self) -> str:
        """Get current branch name, prioritizing environment variables over git commands."""
        logger.debug("Getting current branch")

        # First try environment variable (CI/CD context)
        branch = os.getenv('CI_COMMIT_REF_NAME')
        if branch:
            logger.info(f"Current branch detected from environment: {branch}")
            return branch

        # Fallback to git handler if available
        if self.git_handler:
            try:
                branch = self.git_handler.get_current_branch()
                logger.info(f"Current branch detected from Git: {branch}")
                return branch
            except Exception as e:
                logger.warning(f"Failed to get current branch from git: {e}")

        # If all else fails, we'll need to get it from PR context
        logger.warning("Could not determine current branch from environment or git")
        raise ValueError("Could not determine current branch. Please ensure CI_COMMIT_REF_NAME is set or git is available.")

    async def review_current_pr(self, target_branch: str = 'master', force_regenerate: bool = False) -> Dict[str, Any]:
        """Review the current branch's PR against target branch using selective approach."""
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

            # Get detailed PR information using GetChangeRequest API
            pr_local_id = pr.get('localId')
            if not pr_local_id:
                raise ValueError("PR local ID not found")
            logger.debug(f"Getting detailed PR information for #{pr_local_id}")
            detailed_pr = self.yunxiao_client.get_specific_pull_request(int(pr_local_id))

            logger.info(f"Found PR #{pr_local_id}: {detailed_pr.get('title', 'Unknown title')}")
            return await self.run_selective_review(detailed_pr, target_branch, force_regenerate)

        except Exception as e:
            logger.error(f"Failed to review current PR: {e}")
            raise

    async def review_specific_pr(self, pr_local_id: int, force_regenerate: bool = False) -> Dict[str, Any]:
        """Review a specific PR by its local ID using selective approach."""
        logger.info(f"Starting review for specific PR #{pr_local_id}")

        try:
            # Get detailed PR information using GetChangeRequest API
            logger.debug(f"Fetching detailed PR information for ID: {pr_local_id}")
            pr = self.yunxiao_client.get_specific_pull_request(pr_local_id)

            if not pr:
                logger.error(f"PR with local ID {pr_local_id} not found")
                raise ValueError(f"PR with local ID {pr_local_id} not found")

            logger.info(f"Found PR #{pr_local_id}: {pr.get('title', 'Unknown title')} ({pr.get('sourceBranch')} -> {pr.get('targetBranch')})")
            return await self.run_selective_review(pr, pr.get('targetBranch', 'master'), force_regenerate)

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

        # Get diff content - prioritize Yunxiao API over local git
        logger.debug(f"Getting diff content between {target_branch} and {source_branch}")
        diff_content = self._get_diff_content(pr, target_branch, source_branch)

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
            summary_thinking, summary_result = await self._phase_1_summary(pr, diff_content)
            logger.info(f"Phase 1 completed, summary length: {len(summary_result)} characters")
            await self._post_phase_result_comment(pr_local_id, "Summary Generation", summary_result, to_patch_set_id, summary_thinking)

            # Update PR description with the generated summary
            logger.info("Updating PR description with generated summary")
            await self._update_pr_description(pr_local_id, pr.get('title', 'Unknown'), summary_result)

            # Phase 2: Change Analysis
            logger.info("Starting Phase 2: Change Analysis")
            await self._post_phase_start_comment(pr_local_id, "Change Analysis", to_patch_set_id)
            analysis_thinking, analysis_result = await self._phase_2_analysis(pr, diff_content, summary_result)
            logger.info(f"Phase 2 completed, analysis length: {len(analysis_result)} characters")
            await self._post_phase_result_comment(pr_local_id, "Change Analysis", analysis_result, to_patch_set_id, analysis_thinking)

            # Phase 3: Comment Generation
            logger.info("Starting Phase 3: Comment Generation")
            await self._post_phase_start_comment(pr_local_id, "Comment Generation", to_patch_set_id)
            comments_thinking, comments_raw_result, comments_parsed = await self._phase_3_comments(pr, diff_content, analysis_result)
            logger.info(f"Phase 3 completed, generated {len(comments_parsed)} comments")

            # Post formatted comment result
            await self._post_phase_result_comment(pr_local_id, "Comment Generation", comments_raw_result, to_patch_set_id, comments_thinking)

            # Post inline comments
            await self._post_inline_comments(pr, comments_parsed)

            # Final update after all inline comments are posted
            await self._update_comment_generation_final(pr_local_id, len(comments_parsed))

            # Final summary comment
            logger.info("Posting final summary comment")
            await self._post_final_summary(pr, summary_result, analysis_result, comments_parsed)

            result = {
                'status': 'completed',
                'pr_id': pr_local_id,
                'pr_title': pr['title'],
                'summary': summary_result,
                'analysis': analysis_result,
                'comments_posted': len(comments_parsed),
                'comments': comments_parsed,
                'comments_raw': comments_raw_result
            }

            # Dump review results to JSON file
            try:
                json_file_path = self.json_dumper.dump_results(f"pr_review_{pr_local_id}", result)
                logger.info(f"PR review results dumped to: {json_file_path}")
            except Exception as e:
                logger.error(f"Failed to dump PR review results to JSON: {e}")

            logger.success(f"PR review completed successfully for #{pr_local_id}")
            return result

        except Exception as e:
            logger.error(f"Error during phased review execution: {e}")
            # Post error comment
            await self._post_error_comment(pr_local_id, str(e), to_patch_set_id)
            raise

    async def _phase_1_summary(self, pr: Dict[str, Any], diff_content: str) -> tuple[str, str]:
        """Phase 1: Generate PR summary using system prompt.

        Returns:
            tuple[str, str]: (thinking_content, result_json)
        """
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
        prompt = f"""

PR Title: {context['pr_title']}
PR Description: {context['pr_description']}
Source Branch: {context['source_branch']}
Target Branch: {context['target_branch']}

Git Diff:
{diff_content}

"""

        logger.debug("Phase 1: Sending request to Claude Code SDK")
        try:
            result = await self.claude_runner.run_async(system_prompt, prompt)
            # TODO: only needed when we use claude code 
            #thinking, result = split_thinking_and_json(result)
            result = safe_json_repair(result)
            thinking = ""
            logger.debug(f"Phase 1: Received response from Claude, length: {len(result)} characters")
            logger.debug(f"Phase 1: Thinking content length: {len(thinking or '')} characters")
            return thinking or "", result
        except Exception as e:
            logger.error(f"Phase 1: Claude Code SDK request failed: {e}")
            raise

    async def _phase_2_analysis(self, pr: Dict[str, Any], diff_content: str, summary: str) -> tuple[str, str]:
        """Phase 2: Analyze changes using system prompt.

        Returns:
            tuple[str, str]: (thinking_content, result_json)
        """
        logger.debug("Phase 2: Reading analysis system prompt")
        system_prompt = self.prompt_reader.read_system_prompt('analysis')

        logger.debug(f"Phase 2: Building analysis prompt for PR: {pr.get('title', 'Unknown')}")
        prompt = f"""

Previous Summary:
{summary}

PR Details:
- Title: {pr.get('title', 'Unknown')}
- Description: {pr.get('description', 'No description')}
- Source Branch: {pr.get('sourceBranch', 'unknown')}
- Target Branch: {pr.get('targetBranch', 'unknown')}

Git Diff:
{diff_content}

"""

        logger.debug("Phase 2: Sending analysis request to Claude Code SDK")
        try:
            result = await self.claude_runner.run_async(system_prompt, prompt)
            #thinking, result = split_thinking_and_json(result)
            thinking = ""
            result = safe_json_repair(result)
            logger.debug(f"Phase 2: Received analysis response from Claude, length: {len(result)} characters")
            logger.debug(f"Phase 2: Thinking content length: {len(thinking or '')} characters")
            return thinking or "", result
        except Exception as e:
            logger.error(f"Phase 2: Claude Code SDK analysis request failed: {e}")
            raise

    async def _phase_3_comments(self, pr: Dict[str, Any], diff_content: str, analysis: str) -> tuple[str, str, List[Dict[str, Any]]]:
        """Phase 3: Generate specific comments using system prompt.

        Returns:
            tuple[str, str, List[Dict[str, Any]]]: (thinking_content, result_json, parsed_comments)
        """
        logger.debug("Phase 3: Reading comment system prompt")
        system_prompt = self.prompt_reader.read_system_prompt('comment')

        logger.debug(f"Phase 3: Building comment generation prompt for PR: {pr.get('title', 'Unknown')}")
        prompt = f"""
Previous Analysis:
{analysis}

PR Details:
- Title: {pr.get('title', 'Unknown')}
- Description: {pr.get('description', 'No description')}

Git Diff:
{diff_content}
"""

        logger.debug("Phase 3: Sending comment generation request to Claude Code SDK")
        # try:
        result = await self.claude_runner.run_async(system_prompt, prompt, max_turns=10)
        #thinking, json_block = split_thinking_and_json(result)
        thinking = ""
        json_block = safe_json_repair(result)
        logger.debug(f"Phase 3: Received comment response from Claude, length: {len(json_block)} characters")
        logger.debug(f"Phase 3: Thinking content length: {len(thinking or '')} characters")

        logger.debug("Phase 3: Parsing comment response")
        comments = self._parse_comment_response(json_block)
        logger.debug(f"Phase 3: Parsed {len(comments)} comments from response")
        return thinking or "", result, comments
        # except Exception as e:
        #     logger.error(f"Phase 3: Claude Code SDK comment generation failed: {e}")
        #     raise

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

    async def _post_phase_result_comment(self, pr_local_id: int, phase_name: str, result: str, patch_set_id: str, thinking: str = ""):
        """Update the phase comment with the result and optional thinking tokens."""
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

            # Format the result based on phase type, including thinking tokens
            formatted_result = result
            if phase_name.lower() == "summary generation":
                try:
                    # Use output formatter to create markdown table for summary with thinking
                    formatted_result = self.output_formatter.format_summary_result_with_thinking(result, thinking)
                    logger.debug("Successfully formatted summary result with markdown tables and thinking")
                except Exception as format_error:
                    logger.warning(f"Failed to format summary result, using raw result: {format_error}")
                    formatted_result = result
            elif phase_name.lower() == "change analysis":
                try:
                    # Use output formatter to create markdown table for analysis with thinking
                    formatted_result = self.output_formatter.format_analysis_result_with_thinking(result, thinking)
                    logger.debug("Successfully formatted analysis result with markdown tables and thinking")
                except Exception as format_error:
                    logger.warning(f"Failed to format analysis result, using raw result: {format_error}")
                    formatted_result = result
            elif phase_name.lower() == "comment generation":
                try:
                    # Use output formatter to create markdown table for comments with thinking
                    formatted_result = self.output_formatter.format_comment_result_with_thinking(result, thinking)
                    logger.debug("Successfully formatted comment result with markdown tables and thinking")
                except Exception as format_error:
                    logger.warning(f"Failed to format comment result, using raw result: {format_error}")
                    formatted_result = result

            if comment_biz_id:
                # Update existing comment
                logger.debug(f"Updating existing comment {comment_biz_id} for phase {phase_name}")
                self.yunxiao_client.update_pr_comment(
                    pr_local_id,
                    comment_biz_id,
                    content=f"✅ **{phase_name} Complete**{elapsed_str}\n\n{formatted_result}"
                )
                logger.debug(f"Successfully updated phase result comment for {phase_name}")
            else:
                # Fallback to creating new comment if ID not found
                logger.warning(f"No stored comment ID for phase {phase_name}, creating new comment")
                self.yunxiao_client.create_global_comment(
                    pr_local_id,
                    f"✅ **{phase_name} Complete**{elapsed_str}\n\n{formatted_result}",
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
                    # Handle line ranges (e.g., "22-30") by taking the first line
                    line_str = str(comment['line']).strip()
                    if '-' in line_str:
                        # Extract first line from range
                        try:
                            line_number = int(line_str.split('-')[0])
                            logger.debug(f"Line range detected ({line_str}), using first line: {line_number}")
                        except (ValueError, IndexError) as e:
                            logger.warning(f"Invalid line range format '{line_str}', skipping comment: {e}")
                            continue
                    else:
                        try:
                            line_number = int(line_str)
                        except ValueError as e:
                            logger.warning(f"Invalid line number format '{line_str}', skipping comment: {e}")
                            continue

                    self.yunxiao_client.create_inline_comment(
                        pr_local_id,
                        f"**{comment.get('type', 'COMMENT')}**: {comment['content']}",
                        comment['file'],
                        line_number,
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

- **Summary**: {len(summary.split())} words
- **Analysis**: {len(analysis.split())} words
- **Comments Generated**: {len(comments)}
- **PR Description**: Updated with automated summary
"""

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

    def _get_diff_content(self, pr: Dict[str, Any], target_branch: str, source_branch: str, from_patch_set_id: Optional[str] = None) -> str:
        """Get diff content using Yunxiao API first, fallback to git if needed."""

        if from_patch_set_id:
            # Incremental diff using patch sets
            to_patch_set_id = pr.get('toPatchSetId')
            logger.debug(f"Getting incremental diff for PR #{pr['localId']} from {from_patch_set_id} to {to_patch_set_id}")
            try:
                changes = self.yunxiao_client.get_pull_request_changes(pr['localId'], from_patch_set_id, to_patch_set_id)
                diff_content = self._convert_change_tree_to_diff(changes)
                if diff_content:
                    logger.info(f"Retrieved incremental diff from patch sets, size: {len(diff_content)} characters")
                    return diff_content
            except Exception as e:
                logger.warning(f"Could not get incremental diff: {e}. Falling back to branch diff.")

        # Full diff
        logger.debug(f"Getting full diff content: {target_branch}..{source_branch}")

        try:
            logger.debug(f"Using branch comparison API: {target_branch} -> {source_branch}")
            diff_content = self.yunxiao_client.get_diff_content_from_compare(
                target_branch, source_branch, 'branch', 'branch'
            )

            if diff_content:
                logger.info(f"Retrieved diff from branch comparison, size: {len(diff_content)} characters")
                return diff_content

        except Exception as e:
            logger.warning(f"Yunxiao API diff retrieval failed: {e}")
            if not self.git_handler:
                logger.error("No git handler available for fallback")
                raise

        # Fallback to git handler if available
        if self.git_handler:
            logger.debug("Falling back to git handler for diff")
            try:
                diff = self.git_handler.get_branch_diff(target_branch, source_branch)
                logger.info(f"Retrieved diff using git fallback, size: {len(diff)} characters")
                return diff
            except Exception as e:
                logger.error(f"Git fallback also failed: {e}")
                raise

        raise ValueError("No method available to retrieve diff content")

    def _convert_change_tree_to_diff(self, changes: Dict[str, Any]) -> str:
        """Convert Yunxiao change tree format to unified diff format."""
        logger.debug("Converting change tree to diff format")

        changed_items = changes.get('changedTreeItems', [])
        if not changed_items:
            logger.debug("No changed items found in change tree")
            return ""

        # For now, return a summary format since we don't have the actual diff content
        # In a full implementation, you might need to fetch individual file diffs
        diff_lines = []
        diff_lines.append("# Changes Summary from Yunxiao API")
        diff_lines.append(f"# Total files changed: {changes.get('count', 0)}")
        diff_lines.append(f"# Total additions: {changes.get('totalAddLines', 0)}")
        diff_lines.append(f"# Total deletions: {changes.get('totalDelLines', 0)}")
        diff_lines.append("")

        for item in changed_items:
            file_path = item.get('newPath', item.get('oldPath', 'unknown'))
            add_lines = item.get('addLines', 0)
            del_lines = item.get('delLines', 0)

            if item.get('newFile'):
                diff_lines.append(f"diff --git a/{file_path} b/{file_path}")
                diff_lines.append("new file mode 100644")
                diff_lines.append("--- /dev/null")
                diff_lines.append(f"+++ b/{file_path}")
                diff_lines.append(f"@@ -0,0 +1,{add_lines} @@")
                diff_lines.append(f"# New file with {add_lines} lines added")
            elif item.get('deletedFile'):
                diff_lines.append(f"diff --git a/{file_path} b/{file_path}")
                diff_lines.append("deleted file mode 100644")
                diff_lines.append(f"--- a/{file_path}")
                diff_lines.append("+++ /dev/null")
                diff_lines.append(f"@@ -1,{del_lines} +0,0 @@")
                diff_lines.append(f"# File deleted with {del_lines} lines removed")
            else:
                diff_lines.append(f"diff --git a/{file_path} b/{file_path}")
                diff_lines.append(f"--- a/{file_path}")
                diff_lines.append(f"+++ b/{file_path}")
                diff_lines.append(f"@@ -{del_lines},{del_lines} +{add_lines},{add_lines} @@")
                diff_lines.append(f"# Modified file: +{add_lines} -{del_lines}")

            diff_lines.append("")

        result = "\n".join(diff_lines)
        logger.debug(f"Converted change tree to diff format, size: {len(result)} characters")
        return result

    def _parse_comment_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse Claude's comment response into structured comment data."""
        logger.debug(f"Parsing comment response, length: {len(response)} characters")
        comments = []

        try:
            # Try to parse as JSON first (new format)
            import json
            comment_data = json.loads(response)
            code_suggestions = comment_data.get('code_suggestions', [])

            # Convert new JSON format to the expected inline comment format
            for suggestion in code_suggestions:
                # Extract fields from new format
                relevant_file = suggestion.get('relevant_file', '')
                line_number = suggestion.get('line_number', '')
                label = suggestion.get('label', 'other')
                one_sentence_summary = suggestion.get('one_sentence_summary', '')
                suggestion_content = suggestion.get('suggestion_content', '')
                improved_code = suggestion.get('improved_code', '')

                # Use label directly as comment type
                comment_type = label

                # Build content with suggestion details
                content_parts = []
                if one_sentence_summary:
                    content_parts.append(f"**{one_sentence_summary}**")
                if suggestion_content:
                    content_parts.append(f"\n{suggestion_content}")
                if improved_code:
                    content_parts.append(f"\n\n**Suggested improvement:**\n```\n{improved_code}\n```")

                content = "".join(content_parts)

                # Create comment object
                comment = {
                    'file': relevant_file,
                    'line': line_number,  # Use line_number from new format
                    'type': comment_type,
                    'content': content,
                    'label': label  # Keep label for additional context
                }
                comments.append(comment)

            logger.debug(f"Parsed {len(comments)} comments from new JSON format")
            return comments

        except json.JSONDecodeError:
            # Fallback to old line-based parsing for backward compatibility
            logger.debug("JSON parsing failed, falling back to line-based parsing")
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

            logger.debug(f"Parsed {len(comments)} comments from line-based response")
            return comments

    def _get_comment_type_from_score(self, score: int) -> str:
        """Convert suggestion score to comment type."""
        if score >= 8:
            return "MUST_FIX"
        elif score >= 4:
            return "SHOULD_FIX"
        else:
            return "SUGGESTION"



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
                           "Please review all comments and address any issues marked as MUST_FIX or SHOULD_FIX."
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

    async def _update_pr_description(self, pr_local_id: int, original_title: str, summary: str):
        """Update the PR description with the generated summary."""
        logger.debug(f"Updating PR #{pr_local_id} description with generated summary")
        try:
            # Format the summary using the output formatter
            try:
                formatted_summary = self.output_formatter.format_summary_result(summary)
                logger.debug("Successfully formatted summary for PR description")
            except Exception as format_error:
                logger.warning(f"Failed to format summary for PR description, using raw summary: {format_error}")
                formatted_summary = summary

            # Create a comprehensive description that includes the formatted summary
            updated_description = f"""## Automated Review Summary

{formatted_summary}

---
_This description was automatically generated by the PR review system which developed by **Heng Li** with Claude Code._"""

            result = self.yunxiao_client.update_pull_request(
                pr_local_id,
                title=original_title,  # Keep the original title
                description=updated_description
            )

            if result.get('result'):
                logger.info(f"Successfully updated PR #{pr_local_id} description with formatted summary")
            else:
                logger.warning(f"PR description update returned false result: {result}")

        except Exception as e:
            logger.error(f"Failed to update PR #{pr_local_id} description: {e}")