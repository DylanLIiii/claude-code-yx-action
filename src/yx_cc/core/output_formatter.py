"""Output formatting utilities for code review results."""

import json
from typing import Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class ReviewResult:
    """Structure for code review results."""
    commit_id: str
    summary: str
    analysis: str
    comments: list[Dict[str, Any]]
    metadata: Dict[str, Any]


class OutputFormatter:
    """Formats code review output in different formats."""
    
    def __init__(self, format_type: str = 'markdown'):
        """Initialize with output format type."""
        self.format_type = format_type
    
    def format_result(self, result: ReviewResult) -> str:
        """Format review result according to specified format."""
        if self.format_type == 'json':
            return self._format_json(result)
        elif self.format_type == 'markdown':
            return self._format_markdown(result)
        else:
            raise ValueError(f"Unsupported format type: {self.format_type}")
    
    def _format_json(self, result: ReviewResult) -> str:
        """Format result as JSON."""
        return json.dumps(asdict(result), indent=2, ensure_ascii=False)
    
    def _format_markdown(self, result: ReviewResult) -> str:
        """Format result as Markdown."""
        md_output = []
        
        # Header
        md_output.append(f"# Code Review Report")
        md_output.append(f"**Commit ID:** `{result.commit_id}`")
        md_output.append("")
        
        # Summary section
        md_output.append("## Summary")
        md_output.append(result.summary)
        md_output.append("")
        
        # Analysis section
        md_output.append("## Analysis")
        md_output.append(result.analysis)
        md_output.append("")
        
        # Comments section
        if result.comments:
            md_output.append("## Comments")
            for i, comment in enumerate(result.comments, 1):
                md_output.append(f"### Comment {i}")
                md_output.append(f"**File:** `{comment.get('file', 'Unknown')}`")
                md_output.append(f"**Line:** {comment.get('line', 'N/A')}")
                md_output.append("")
                md_output.append(comment.get('content', ''))
                md_output.append("")
        
        # Metadata
        if result.metadata:
            md_output.append("## Metadata")
            for key, value in result.metadata.items():
                md_output.append(f"- **{key}:** {value}")
        
        return "\n".join(md_output)