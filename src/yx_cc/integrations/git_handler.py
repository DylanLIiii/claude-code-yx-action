"""Git operations handler for retrieving commit information and diffs."""

import subprocess
import json
from datetime import datetime
from typing import Dict, List, Any


class GitHandler:
    """Handles Git operations for code review."""
    
    def get_commit_info(self, commit_id: str) -> Dict[str, Any]:
        """Get detailed commit information."""
        try:
            # Get commit metadata
            cmd = [
                'git', 'show', '--format=fuller', '--name-status', 
                '--no-patch', commit_id
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Parse commit info
            lines = result.stdout.strip().split('\n')
            commit_info = self._parse_commit_output(lines)
            commit_info['commit_id'] = commit_id
            
            return commit_info
            
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Failed to get commit info for {commit_id}: {e}")
    
    def get_commit_diff(self, commit_id: str) -> str:
        """Get the diff content for a commit."""
        try:
            cmd = ['git', 'show', '--format=', commit_id]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout
            
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Failed to get diff for {commit_id}: {e}")
    
    def get_file_diff(self, commit_id: str, file_path: str) -> str:
        """Get diff for a specific file."""
        try:
            cmd = ['git', 'show', f'{commit_id}:{file_path}']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout
            
        except subprocess.CalledProcessError as e:
            return f"Error getting file content: {e}"
    
    def get_current_timestamp(self) -> str:
        """Get current timestamp for metadata."""
        return datetime.now().isoformat()
    
    def _parse_commit_output(self, lines: List[str]) -> Dict[str, Any]:
        """Parse git show output into structured data."""
        commit_info = {}
        files = []
        
        for line in lines:
            if line.startswith('Author:'):
                commit_info['author'] = line.split(':', 1)[1].strip()
            elif line.startswith('Date:'):
                commit_info['date'] = line.split(':', 1)[1].strip()
            elif line.startswith('CommitDate:'):
                commit_info['commit_date'] = line.split(':', 1)[1].strip()
            elif line.startswith('    '):  # Commit message lines
                if 'message' not in commit_info:
                    commit_info['message'] = ''
                commit_info['message'] += line[4:] + '\n'
            elif '\t' in line and any(line.startswith(status) for status in ['A', 'M', 'D', 'R', 'C']):
                # File status line
                status, filename = line.split('\t', 1)
                files.append({'status': status, 'filename': filename})
        
        if 'message' in commit_info:
            commit_info['message'] = commit_info['message'].strip()
        
        commit_info['files'] = files
        return commit_info
    
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
    
    def fetch_origin(self) -> bool:
        """Fetch latest changes from origin remote."""
        try:
            result = subprocess.run(
                ['git', 'fetch', 'origin'],
                capture_output=True, text=True, check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Failed to fetch from origin: {e}")
    
    def get_branch_diff(self, base_branch: str, target_branch: str) -> str:
        """Get diff between two branches."""
        try:
            cmd = ['git', 'diff', f'origin/{base_branch}..origin/{target_branch}']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Failed to get diff between {base_branch} and {target_branch}: {e}")
    
    def get_branch_diff_summary(self, base_branch: str, target_branch: str) -> Dict[str, Any]:
        """Get summary of changes between two branches."""
        try:
            # Get file stats
            cmd = ['git', 'diff', '--stat', f'origin/{base_branch}..origin/{target_branch}']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            stat_output = result.stdout
            
            # Get list of changed files with their status
            cmd = ['git', 'diff', '--name-status', f'origin/{base_branch}..origin/{target_branch}']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            files = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        status = parts[0]
                        filename = parts[1]
                        files.append({'status': status, 'filename': filename})
            
            return {
                'stat_summary': stat_output,
                'changed_files': files,
                'base_branch': base_branch,
                'target_branch': target_branch
            }
            
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Failed to get diff summary between {base_branch} and {target_branch}: {e}")