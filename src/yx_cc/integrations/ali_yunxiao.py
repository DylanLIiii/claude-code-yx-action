"""Ali YunXiao API client for repository management and PR operations."""

import os
import requests
from typing import Dict, Any, Optional, List
import json
import urllib.parse
import asyncio

from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions



class _ClaudeRunner:
    """Internal helper to run Claude Code SDK calls synchronously."""

    @staticmethod
    def run(system_prompt: str, prompt: str, max_turns: int = 2) -> str:
        async def _run() -> str:
            async with ClaudeSDKClient(
                options=ClaudeCodeOptions(
                    system_prompt=system_prompt,
                    permission_mode='plan',
                    max_turns=max_turns,
                )
            ) as client:
                await client.query(prompt)
                chunks = []
                async for message in client.receive_response():
                    if hasattr(message, 'content'):
                        for block in getattr(message, 'content', []) or []:
                            if hasattr(block, 'text') and isinstance(block.text, str):
                                chunks.append(block.text)
                return ''.join(chunks).strip()
        return asyncio.run(_run())




class AliYunXiaoClient:
    """Client for Ali YunXiao repository management API."""

    def __init__(self):
        """Initialize client with environment variables."""
        self.domain = os.getenv('ALI_YUNXIAO_DOMAIN', 'openapi-rdc.aliyuncs.com')
        self.token = os.getenv('ALI_YUNXIAO_TOKEN')
        self.organization_id = os.getenv('ALI_ORGANIZATION_ID')
        self.repository_id = os.getenv('ALI_REPOSITORY_ID')

        if not self.token:
            raise ValueError(
                "Ali YunXiao token not found. Set ALI_YUNXIAO_TOKEN environment variable."
            )
        if not self.organization_id:
            raise ValueError(
                "Organization ID not found. Set ALI_ORGANIZATION_ID environment variable."
            )
        if not self.repository_id:
            raise ValueError(
                "Repository ID not found. Set ALI_REPOSITORY_ID environment variable."
            )

    def get_pull_requests(self, state: str = None, page: int = 1, per_page: int = 10) -> List[Dict[str, Any]]:
        """Get list of pull requests for the repository."""
        params = {
            'page': page,
            'perPage': per_page,
            'projectIds': self.repository_id
        }
        if state:
            params['state'] = state

        endpoint = f'/oapi/v1/codeup/organizations/{self.organization_id}/changeRequests'
        return self._make_request('GET', endpoint, params=params)

    def get_pull_request_changes(self, local_id: int, from_patch_set_id: str, to_patch_set_id: str) -> Dict[str, Any]:
        """Get changes for a specific pull request."""
        params = {
            'fromPatchSetId': from_patch_set_id,
            'toPatchSetId': to_patch_set_id
        }

        endpoint = f'/oapi/v1/codeup/organizations/{self.organization_id}/repositories/{self.repository_id}/changeRequests/{local_id}/diffs/changeTree'
        return self._make_request('GET', endpoint, params=params)

    def get_branch_info(self, branch_name: str) -> Dict[str, Any]:
        """Get information about a specific branch."""
        encoded_branch = urllib.parse.quote(branch_name, safe='')
        endpoint = f'/oapi/v1/codeup/organizations/{self.organization_id}/repositories/{self.repository_id}/branches/{encoded_branch}'
        return self._make_request('GET', endpoint)

    def create_pr_comment(self, local_id: int, comment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comment on a pull request."""
        endpoint = f'/oapi/v1/codeup/organizations/{self.organization_id}/repositories/{self.repository_id}/changeRequests/{local_id}/comments'
        return self._make_request('POST', endpoint, data=comment_data)

    def update_pr_comment(self, local_id: int, comment_biz_id: str, content: str = None, resolved: bool = None) -> Dict[str, Any]:
        """Update an existing PR comment."""
        data = {}
        if content is not None:
            data['content'] = content
        if resolved is not None:
            data['resolved'] = resolved

        endpoint = f'/oapi/v1/codeup/organizations/{self.organization_id}/repositories/{self.repository_id}/changeRequests/{local_id}/comments/{comment_biz_id}'
        return self._make_request('PUT', endpoint, data=data)

    def update_pull_request(self, local_id: int, title: str = None, description: str = None) -> Dict[str, Any]:
        """Update pull request basic information."""
        data = {}
        if title is not None:
            data['title'] = title
        if description is not None:
            data['description'] = description

        endpoint = f'/oapi/v1/codeup/organizations/{self.organization_id}/repositories/{self.repository_id}/changeRequests/{local_id}'
        return self._make_request('PUT', endpoint, data=data)

    def get_branches(self, page: int = 1, per_page: int = 10, search: str = None) -> List[Dict[str, Any]]:
        """Get list of branches for the repository."""
        params = {
            'page': page,
            'perPage': per_page
        }
        if search:
            params['search'] = search

        endpoint = f'/oapi/v1/codeup/organizations/{self.organization_id}/repositories/{self.repository_id}/branches'
        return self._make_request('GET', endpoint, params=params)

    def _make_request(self, method: str, endpoint: str, params: Dict[str, Any] = None, data: Dict[str, Any] = None) -> Any:
        """Make authenticated request to Ali YunXiao API."""
        url = f"https://{self.domain}{endpoint}"

        headers = {
            'Content-Type': 'application/json',
            'x-yunxiao-token': self.token
        }

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, json=data, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            raise RuntimeError(f"YunXiao API request failed: {e}")

    def create_global_comment(self, local_id: int, content: str, patch_set_biz_id: str, resolved: bool = False, draft: bool = False) -> Dict[str, Any]:
        """Create a global comment on a pull request."""
        data = {
            'comment_type': 'GLOBAL_COMMENT',
            'content': content,
            'patchset_biz_id': patch_set_biz_id,
            'resolved': resolved,
            'draft': draft
        }
        return self.create_pr_comment(local_id, data)

    def create_inline_comment(self, local_id: int, content: str, file_path: str, line_number: int,
                             from_patch_set_id: str, to_patch_set_id: str, resolved: bool = False, draft: bool = False) -> Dict[str, Any]:
        """Create an inline comment on a specific line in a pull request."""
        data = {
            'comment_type': 'INLINE_COMMENT',
            'content': content,
            'file_path': file_path,
            'line_number': line_number,
            'from_patchset_biz_id': from_patch_set_id,
            'to_patchset_biz_id': to_patch_set_id,
            'patchset_biz_id': to_patch_set_id,  # Usually the target patch set
            'resolved': resolved,
            'draft': draft
        }
        return self.create_pr_comment(local_id, data)

    def get_current_branch_from_env(self) -> str:
        """Get current branch name from CI environment variable."""
        branch = os.getenv('CI_COMMIT_REF_NAME')
        if not branch:
            raise ValueError("CI_COMMIT_REF_NAME environment variable not set")
        return branch

    def find_pull_request_by_branch(self, source_branch: str, target_branch: str = 'master') -> Optional[Dict[str, Any]]:
        """Find pull request by source and target branch."""
        prs = self.get_pull_requests(state='opened')

        for pr in prs:
            if (pr.get('sourceBranch') == source_branch and
                pr.get('targetBranch') == target_branch):
                return pr

    # ----------------------------------------
    # AI Code Review helpers (Claude Code SDK)
    # ----------------------------------------
    def generate_summary(self, system_prompt: str, commit_info: Dict[str, Any], diff_content: str) -> str:
        """Generate a PR/commit summary using Claude Code SDK."""
        prompt = self._build_summary_prompt(commit_info, diff_content)
        return _ClaudeRunner.run(system_prompt=system_prompt, prompt=prompt, max_turns=2)

    def analyze_changes(self, system_prompt: str, commit_info: Dict[str, Any], diff_content: str, summary: str) -> str:
        """Analyze changes using Claude Code SDK and return analysis text."""
        prompt = self._build_analysis_prompt(commit_info, diff_content, summary)
        return _ClaudeRunner.run(system_prompt=system_prompt, prompt=prompt, max_turns=2)

    def generate_comments(self, system_prompt: str, commit_info: Dict[str, Any], diff_content: str, analysis: str) -> List[Dict[str, Any]]:
        """Generate structured inline comments using Claude Code SDK.

        Returns a list of dicts with keys: file, line, content
        """
        prompt = self._build_comments_prompt(commit_info, diff_content, analysis)
        raw = _ClaudeRunner.run(system_prompt=system_prompt, prompt=prompt, max_turns=2)
        comments = self._try_parse_comments_json(raw)
        if comments is not None:
            return comments
        # Fallback: simple line-based parse
        return self._fallback_parse_comments(raw)

    # -----------
    # Prompt builders
    # -----------
    def _build_summary_prompt(self, commit_info: Dict[str, Any], diff_content: str) -> str:
        files = commit_info.get('files', [])
        files_desc = "\n".join([f"- {f.get('status','?')} {f.get('filename','')}" for f in files])
        return (
            f"You are an experienced reviewer. Generate a concise summary for this change.\n\n"
            f"Commit Author: {commit_info.get('author','Unknown')}\n"
            f"Commit Date: {commit_info.get('date', commit_info.get('commit_date','Unknown'))}\n"
            f"Commit Message:\n{commit_info.get('message','(no message)')}\n\n"
            f"Files Changed:\n{files_desc}\n\n"
            f"Git Diff:\n{diff_content}\n\n"
            f"Output: 3-6 bullet points summarizing the intent and scope."
        )

    def _build_analysis_prompt(self, commit_info: Dict[str, Any], diff_content: str, summary: str) -> str:
        return (
            "You are reviewing a code change. Using the provided summary and diff, "
            "identify potential issues, risky areas, and improvement suggestions.\n\n"
            f"SUMMARY PROVIDED:\n{summary}\n\n"
            f"COMMIT MESSAGE:\n{commit_info.get('message','(no message)')}\n\n"
            f"GIT DIFF:\n{diff_content}\n\n"
            "Return a structured analysis with sections: 'Risks', 'Findings', 'Suggestions'."
        )

    def _build_comments_prompt(self, commit_info: Dict[str, Any], diff_content: str, analysis: str) -> str:
        return (
            "Based on the analysis and the diff, propose inline review comments. "
            "Return STRICT JSON array named 'comments' (no extra text) where each item has keys: "
            "'file' (string path), 'line' (integer line number if known else 0), 'content' (string).\n\n"
            f"ANALYSIS:\n{analysis}\n\n"
            f"DIFF:\n{diff_content}\n\n"
            "JSON ONLY. Example: {\"comments\":[{\"file\":\"src/app.py\",\"line\":42,\"content\":\"Prefer using with-statement for file IO\"}]]"
        )

    # -----------
    # Parsing helpers
    # -----------
    def _try_parse_comments_json(self, raw: str) -> Optional[List[Dict[str, Any]]]:
        try:
            data = json.loads(raw)
            arr = data.get('comments') if isinstance(data, dict) else data
            if isinstance(arr, list):
                cleaned: List[Dict[str, Any]] = []
                for item in arr:
                    if not isinstance(item, dict):
                        continue
                    file_path = item.get('file')
                    line = item.get('line')
                    content = item.get('content')
                    if file_path and content:
                        try:
                            line_int = int(line) if line is not None else 0
                        except (TypeError, ValueError):
                            line_int = 0
                        cleaned.append({'file': file_path, 'line': line_int, 'content': content})
                return cleaned
        except Exception:
            return None
        return None

    def _fallback_parse_comments(self, response: str) -> List[Dict[str, Any]]:
        comments: List[Dict[str, Any]] = []
        for line in response.splitlines():
            line = line.strip()
            # Expect format: - File: path, Line: 42, Comment: text
            if line.startswith('- '):
                parts = line[2:].split(', ')
                file_part = next((p for p in parts if p.lower().startswith('file:')), None)
                line_part = next((p for p in parts if p.lower().startswith('line:')), None)
                comment_part = next((p for p in parts if p.lower().startswith('comment:')), None)
                content = (comment_part.split(':', 1)[1].strip() if comment_part else line[2:])
                try:
                    line_num = int(line_part.split(':', 1)[1].strip()) if line_part else 0
                except Exception:
                    line_num = 0
                comments.append({
                    'file': file_part.split(':', 1)[1].strip() if file_part else '',
                    'line': line_num,
                    'content': content
                })
        if not comments:
            # Fallback to a single global-style comment
            comments.append({'file': '', 'line': 0, 'content': response[:2000]})
        return comments
