"""Ali YunXiao API client for repository management and PR operations."""

import os
import requests
from typing import Dict, Any, Optional, List
import urllib.parse
from loguru import logger


class AliYunXiaoClient:
    """Client for Ali YunXiao repository management API."""

    def __init__(self):
        """Initialize client with environment variables."""
        logger.info("Initializing Ali YunXiao client")

        self.domain = os.getenv('ALI_YUNXIAO_DOMAIN', 'openapi-rdc.aliyuncs.com')
        self.token = os.getenv('ALI_YUNXIAO_TOKEN')
        self.organization_id = os.getenv('ALI_ORGANIZATION_ID')
        self.repository_id = os.getenv('ALI_REPOSITORY_ID')

        logger.debug(f"Using domain: {self.domain}")
        logger.debug(f"Organization ID: {self.organization_id}")
        logger.debug(f"Repository ID: {self.repository_id}")

        if not self.token:
            logger.error("Ali YunXiao token not found in environment variables")
            raise ValueError(
                "Ali YunXiao token not found. Set ALI_YUNXIAO_TOKEN environment variable."
            )
        if not self.organization_id:
            logger.error("Organization ID not found in environment variables")
            raise ValueError(
                "Organization ID not found. Set ALI_ORGANIZATION_ID environment variable."
            )
        if not self.repository_id:
            logger.error("Repository ID not found in environment variables")
            raise ValueError(
                "Repository ID not found. Set ALI_REPOSITORY_ID environment variable."
            )

        logger.info("Ali YunXiao client initialized successfully")

    def get_pull_requests(self, state: Optional[str] = None, page: int = 1, per_page: int = 10) -> List[Dict[str, Any]]:
        """Get list of pull requests for the repository."""
        logger.debug(f"Getting pull requests: state={state}, page={page}, per_page={per_page}")

        params = {
            'page': page,
            'perPage': per_page,
            'projectIds': self.repository_id
        }
        if state:
            params['state'] = state

        endpoint = f'/oapi/v1/codeup/organizations/{self.organization_id}/changeRequests'

        try:
            result = self._make_request('GET', endpoint, params=params)
            logger.info(f"Retrieved {len(result) if isinstance(result, list) else 'unknown'} pull requests")
            return result
        except Exception as e:
            logger.error(f"Failed to get pull requests: {e}")
            raise

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

    def _make_request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None) -> Any:
        """Make authenticated request to Ali YunXiao API."""
        url = f"https://{self.domain}{endpoint}"

        logger.debug(f"Making {method} request to: {endpoint}")
        if params:
            logger.debug(f"Request params: {params}")
        if data:
            logger.debug(f"Request data keys: {list(data.keys())}")

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
                logger.error(f"Unsupported HTTP method: {method}")
                raise ValueError(f"Unsupported HTTP method: {method}")

            logger.debug(f"Response status: {response.status_code}")
            response.raise_for_status()

            result = response.json()
            logger.debug(f"Request successful, response type: {type(result)}")
            return result

        except requests.RequestException as e:
            logger.error(f"YunXiao API request failed for {method} {endpoint}: {e}")
            raise RuntimeError(f"YunXiao API request failed: {e}")

    def create_global_comment(self, local_id: int, content: str, patch_set_biz_id: str, resolved: bool = False, draft: bool = False) -> Dict[str, Any]:
        """Create a global comment on a pull request."""
        logger.debug(f"Creating global comment on PR #{local_id}, content length: {len(content)}")

        data = {
            'comment_type': 'GLOBAL_COMMENT',
            'content': content,
            'patchset_biz_id': patch_set_biz_id,
            'resolved': resolved,
            'draft': draft
        }

        try:
            result = self.create_pr_comment(local_id, data)
            logger.info(f"Successfully created global comment on PR #{local_id}")
            return result
        except Exception as e:
            logger.error(f"Failed to create global comment on PR #{local_id}: {e}")
            raise

    def create_inline_comment(self, local_id: int, content: str, file_path: str, line_number: int,
                             from_patch_set_id: str, to_patch_set_id: str, resolved: bool = False, draft: bool = False) -> Dict[str, Any]:
        """Create an inline comment on a specific line in a pull request."""
        logger.debug(f"Creating inline comment on PR #{local_id} at {file_path}:{line_number}")

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

        try:
            result = self.create_pr_comment(local_id, data)
            logger.info(f"Successfully created inline comment on PR #{local_id} at {file_path}:{line_number}")
            return result
        except Exception as e:
            logger.error(f"Failed to create inline comment on PR #{local_id} at {file_path}:{line_number}: {e}")
            raise



    def find_pull_request_by_branch(self, source_branch: str, target_branch: str = 'master') -> Optional[Dict[str, Any]]:
        """Find pull request by source and target branch."""
        logger.debug(f"Searching for PR: {source_branch} -> {target_branch}")

        try:
            prs = self.get_pull_requests(state='opened')
            logger.debug(f"Found {len(prs) if isinstance(prs, list) else 'unknown'} open PRs to search")

            for pr in prs:
                if (pr.get('sourceBranch') == source_branch and
                    pr.get('targetBranch') == target_branch):
                    logger.info(f"Found matching PR #{pr.get('localId')}: {pr.get('title', 'Unknown title')}")
                    return pr

            logger.warning(f"No PR found for {source_branch} -> {target_branch}")
            return None

        except Exception as e:
            logger.error(f"Failed to find PR by branch: {e}")
            raise
