"""PR review feature using local Git + YunXiao API + Claude Code SDK."""

import os
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
import asyncio

from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions
from ..integrations.ali_yunxiao import AliYunXiaoClient
from ..integrations.git_handler import GitHandler


class PRReviewer:
    """PR review engine using local Git, YunXiao API, and Claude Code SDK."""
    
    def __init__(self):
        """Initialize PR reviewer with necessary clients."""
        self.yunxiao_client = AliYunXiaoClient()
        self.git_handler = GitHandler()
        
        # Get current branch from environment
        try:
            self.current_branch = self.yunxiao_client.get_current_branch_from_env()
        except ValueError:
            # Fallback to git if CI environment is not available
            self.current_branch = self._get_current_branch_from_git()
    
    async def review_current_pr(self, target_branch: str = 'master') -> Dict[str, Any]:
        """Review the current branch's PR against target branch."""
        # Find the PR for current branch
        pr = self.yunxiao_client.find_pull_request_by_branch(
            source_branch=self.current_branch,
            target_branch=target_branch
        )
        
        if not pr:
            raise ValueError(f"No open PR found for branch {self.current_branch} -> {target_branch}")
        
        # Get local Git diff between branches  
        diff_content = self._get_branch_diff(target_branch, self.current_branch)
        
        if not diff_content.strip():
            return {
                'status': 'no_changes',
                'message': 'No changes detected between branches',
                'pr_id': pr['localId']
            }
        
        # Use Claude Code SDK to analyze the diff
        analysis_result = await self._analyze_diff_with_claude(diff_content, pr)
        
        # Post review comments to YunXiao
        comments_posted = await self._post_review_comments(pr, analysis_result)
        
        return {
            'status': 'completed',
            'pr_id': pr['localId'],
            'pr_title': pr['title'],
            'analysis': analysis_result['summary'],
            'comments_posted': len(comments_posted),
            'comments': comments_posted
        }
    
    async def review_specific_pr(self, pr_local_id: int) -> Dict[str, Any]:
        """Review a specific PR by its local ID."""
        # Get PR details from YunXiao
        prs = self.yunxiao_client.get_pull_requests(state='opened')
        pr = next((p for p in prs if p['localId'] == pr_local_id), None)
        
        if not pr:
            raise ValueError(f"PR with local ID {pr_local_id} not found")
        
        # Get changes from YunXiao API
        try:
            changes = self.yunxiao_client.get_pull_request_changes(
                pr_local_id, 
                pr.get('fromPatchSetId', ''), 
                pr.get('toPatchSetId', '')
            )
        except Exception:
            # Fallback to local Git diff
            diff_content = self._get_branch_diff(pr['targetBranch'], pr['sourceBranch'])
        else:
            diff_content = self._format_changes_to_diff(changes)
        
        # Analyze with Claude Code SDK
        analysis_result = await self._analyze_diff_with_claude(diff_content, pr)
        
        # Post comments
        comments_posted = await self._post_review_comments(pr, analysis_result)
        
        return {
            'status': 'completed',
            'pr_id': pr['localId'],
            'pr_title': pr['title'],
            'analysis': analysis_result['summary'],
            'comments_posted': len(comments_posted),
            'comments': comments_posted
        }
    
    async def _analyze_diff_with_claude(self, diff_content: str, pr: Dict[str, Any]) -> Dict[str, Any]:
        """Use Claude Code SDK to analyze the diff content."""
        system_prompt = """You are a senior code reviewer. Analyze the provided Git diff and:
1. Provide a summary of changes
2. Identify potential issues, bugs, or security concerns
3. Suggest improvements for code quality
4. For each specific issue, provide the file path and line number where possible

Format your response as:
SUMMARY: Brief overview of changes

ISSUES:
- File: path/to/file.py, Line: 42, Issue: Description of issue
- File: path/to/file.py, Line: 89, Issue: Another issue

SUGGESTIONS:
- General suggestions for improvement"""
        
        prompt = f"""Please review this Pull Request:

PR Title: {pr.get('title', 'Unknown')}
PR Description: {pr.get('description', 'No description')}
Source Branch: {pr.get('sourceBranch', 'unknown')}
Target Branch: {pr.get('targetBranch', 'unknown')}

Git Diff:
{diff_content}

Please provide a thorough code review."""
        
        async with ClaudeSDKClient(
            options=ClaudeCodeOptions(
                system_prompt=system_prompt,
                max_turns=2
            )
        ) as client:
            await client.query(prompt)
            
            full_response = []
            async for message in client.receive_response():
                if hasattr(message, 'content'):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            full_response.append(block.text)
        
        response_text = ''.join(full_response)
        return self._parse_claude_response(response_text)
    
    async def _post_review_comments(self, pr: Dict[str, Any], analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Post review comments to YunXiao."""
        comments_posted = []
        pr_local_id = pr['localId']
        
        # Get patch set IDs - use the latest version
        to_patch_set_id = pr.get('toPatchSetId', '')
        from_patch_set_id = pr.get('fromPatchSetId', '')
        
        # Post summary as global comment
        if analysis['summary']:
            try:
                comment = self.yunxiao_client.create_global_comment(
                    pr_local_id,
                    f"## Code Review Summary\n\n{analysis['summary']}",
                    to_patch_set_id
                )
                comments_posted.append({
                    'type': 'global',
                    'content': analysis['summary'],
                    'comment_id': comment.get('comment_biz_id')
                })
            except Exception as e:
                print(f"Failed to post global comment: {e}")
        
        # Post specific issue comments
        for issue in analysis['issues']:
            if issue['file'] and issue['line']:
                try:
                    comment = self.yunxiao_client.create_inline_comment(
                        pr_local_id,
                        issue['content'],
                        issue['file'],
                        int(issue['line']),
                        from_patch_set_id,
                        to_patch_set_id
                    )
                    comments_posted.append({
                        'type': 'inline',
                        'file': issue['file'],
                        'line': issue['line'],
                        'content': issue['content'],
                        'comment_id': comment.get('comment_biz_id')
                    })
                except Exception as e:
                    print(f"Failed to post inline comment for {issue['file']}:{issue['line']}: {e}")
        
        # Post general suggestions as global comment
        if analysis['suggestions']:
            try:
                suggestions_text = "\n".join([f"- {s}" for s in analysis['suggestions']])
                comment = self.yunxiao_client.create_global_comment(
                    pr_local_id,
                    f"## Suggestions for Improvement\n\n{suggestions_text}",
                    to_patch_set_id
                )
                comments_posted.append({
                    'type': 'global',
                    'content': f"Suggestions: {suggestions_text}",
                    'comment_id': comment.get('comment_biz_id')
                })
            except Exception as e:
                print(f"Failed to post suggestions comment: {e}")
        
        return comments_posted
    
    def _get_current_branch_from_git(self) -> str:
        """Get current branch name using Git command."""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Failed to get current branch: {e}")
    
    def _get_branch_diff(self, base_branch: str, compare_branch: str) -> str:
        """Get diff between two branches using Git."""
        try:
            result = subprocess.run(
                ['git', 'diff', f'{base_branch}..{compare_branch}'],
                capture_output=True, text=True, check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Failed to get diff between {base_branch} and {compare_branch}: {e}")
    
    def _format_changes_to_diff(self, changes: Dict[str, Any]) -> str:
        """Format YunXiao changes response to diff-like format."""
        diff_lines = []
        
        for item in changes.get('changedTreeItems', []):
            file_path = item.get('newPath') or item.get('oldPath')
            add_lines = item.get('addLines', 0)
            del_lines = item.get('delLines', 0)
            
            diff_lines.append(f"--- a/{file_path}")
            diff_lines.append(f"+++ b/{file_path}")
            diff_lines.append(f"@@ +{add_lines},-{del_lines} @@")
            
            if item.get('newFile'):
                diff_lines.append(f"New file: {file_path}")
            elif item.get('deletedFile'):
                diff_lines.append(f"Deleted file: {file_path}")
            elif item.get('renamedFile'):
                diff_lines.append(f"Renamed: {item.get('oldPath')} -> {file_path}")
        
        return "\n".join(diff_lines)
    
    def _parse_claude_response(self, response: str) -> Dict[str, Any]:
        """Parse Claude's response into structured data."""
        result = {
            'summary': '',
            'issues': [],
            'suggestions': []
        }
        
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('SUMMARY:'):
                current_section = 'summary'
                result['summary'] = line[8:].strip()
            elif line.startswith('ISSUES:'):
                current_section = 'issues'
            elif line.startswith('SUGGESTIONS:'):
                current_section = 'suggestions'
            elif line.startswith('- ') and current_section:
                if current_section == 'issues':
                    # Parse "File: path, Line: num, Issue: description"
                    issue_parts = line[2:].split(', ')
                    file_part = next((p for p in issue_parts if p.startswith('File:')), None)
                    line_part = next((p for p in issue_parts if p.startswith('Line:')), None)
                    issue_part = next((p for p in issue_parts if p.startswith('Issue:')), None)
                    
                    result['issues'].append({
                        'file': file_part.split(':', 1)[1].strip() if file_part else None,
                        'line': line_part.split(':', 1)[1].strip() if line_part else None,
                        'content': issue_part.split(':', 1)[1].strip() if issue_part else line[2:]
                    })
                elif current_section == 'suggestions':
                    result['suggestions'].append(line[2:])
            elif current_section == 'summary' and line:
                result['summary'] += ' ' + line
        
        return result