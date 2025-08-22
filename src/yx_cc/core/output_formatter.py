"""Output formatting utilities for code review results."""

import json
from typing import Dict, Any, List, Union
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

    def format_summary_result(self, summary_json: str) -> str:
        """Format summary result from PR reviewer into markdown with tables for file descriptions."""
        try:
            # Parse the JSON summary result
            summary_data = json.loads(summary_json)
            return self._format_summary_markdown(summary_data)
        except json.JSONDecodeError as e:
            # If JSON parsing fails, return the raw summary with a note
            return f"## Summary\n\n{summary_json}\n\n_Note: Could not parse as JSON: {e}_"
        except Exception as e:
            # Handle any other formatting errors
            return f"## Summary\n\n{summary_json}\n\n_Note: Formatting error: {e}_"

    def format_analysis_result(self, analysis_json: str) -> str:
        """Format analysis result from PR reviewer into markdown with tables for key issues."""
        try:
            # Parse the JSON analysis result
            analysis_data = json.loads(analysis_json)
            return self._format_analysis_markdown(analysis_data)
        except json.JSONDecodeError as e:
            # If JSON parsing fails, return the raw analysis with a note
            return f"## Analysis\n\n{analysis_json}\n\n_Note: Could not parse as JSON: {e}_"
        except Exception as e:
            # Handle any other formatting errors
            return f"## Analysis\n\n{analysis_json}\n\n_Note: Formatting error: {e}_"

    def format_comment_result(self, comment_json: str) -> str:
        """Format comment result from PR reviewer into markdown with tables for code suggestions."""
        try:
            # Parse the JSON comment result
            comment_data = json.loads(comment_json)
            return self._format_comment_markdown(comment_data)
        except json.JSONDecodeError as e:
            # If JSON parsing fails, return the raw comment with a note
            return f"## Comments\n\n{comment_json}\n\n_Note: Could not parse as JSON: {e}_"
        except Exception as e:
            # Handle any other formatting errors
            return f"## Comments\n\n{comment_json}\n\n_Note: Formatting error: {e}_"

    def format_summary_result_with_thinking(self, summary_json: str, thinking: str) -> str:
        """Format summary result with thinking tokens in a collapsible section."""
        formatted_result = self.format_summary_result(summary_json)
        if thinking and thinking.strip():
            thinking_section = self._format_thinking_section(thinking, "Summary Generation")
            return f"{formatted_result}\n\n{thinking_section}"
        return formatted_result

    def format_analysis_result_with_thinking(self, analysis_json: str, thinking: str) -> str:
        """Format analysis result with thinking tokens in a collapsible section."""
        formatted_result = self.format_analysis_result(analysis_json)
        if thinking and thinking.strip():
            thinking_section = self._format_thinking_section(thinking, "Change Analysis")
            return f"{formatted_result}\n\n{thinking_section}"
        return formatted_result

    def format_comment_result_with_thinking(self, comment_json: str, thinking: str) -> str:
        """Format comment result with thinking tokens in a collapsible section."""
        formatted_result = self.format_comment_result(comment_json)
        if thinking and thinking.strip():
            thinking_section = self._format_thinking_section(thinking, "Comment Generation")
            return f"{formatted_result}\n\n{thinking_section}"
        return formatted_result
    
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

    def _format_summary_markdown(self, summary_data: Dict[str, Any]) -> str:
        """Format parsed summary data as markdown with tables for file descriptions."""
        md_output = []

        # Title
        title = summary_data.get('title', 'PR Summary')
        md_output.append(f"# {title}")
        md_output.append("")

        # PR Type(s)
        pr_types = summary_data.get('type', [])
        if pr_types:
            if isinstance(pr_types, list):
                type_str = ", ".join(pr_types)
            else:
                type_str = str(pr_types)
            md_output.append(f"**Type:** {type_str}")
            md_output.append("")

        # Description
        description = summary_data.get('description', '')
        if description:
            md_output.append("## Description")
            md_output.append(self._format_list_to_markdown(description))
            md_output.append("")

        # Changes Diagram
        changes_diagram = summary_data.get('changes_diagram', '')
        if changes_diagram:
            md_output.append("## Changes Overview")
            md_output.append(changes_diagram)
            md_output.append("")

        # File Changes Table
        pr_files = summary_data.get('pr_files', [])
        if pr_files:
            md_output.append("## File Changes")
            md_output.append("")

            # Create markdown table
            md_output.append("| File | Changes | Label |")
            md_output.append("|------|---------|-------|")

            for file_desc in pr_files:
                filename = file_desc.get('filename', 'Unknown')
                changes_title = file_desc.get('changes_title', 'No title')
                changes_summary = file_desc.get('changes_summary', 'No summary')
                label = file_desc.get('label', 'other')

                # Format changes_summary, which could be a list
                changes_summary = self._format_list_to_markdown(changes_summary)

                # Escape pipe characters in content and format for table
                filename_escaped = filename.replace('|', '\\|')
                changes_title_escaped = changes_title.replace('|', '\\|')
                changes_summary_escaped = changes_summary.replace('|', '\\|').replace('\n', '<br>')
                label_escaped = label.replace('|', '\\|')

                # Combine title and summary for the changes column
                changes_content = f"**{changes_title_escaped}**<br>{changes_summary_escaped}"

                md_output.append(f"| `{filename_escaped}` | {changes_content} | `{label_escaped}` |")

            md_output.append("")

        return "\n".join(md_output)

    def _format_analysis_markdown(self, analysis_data: Dict[str, Any]) -> str:
        """Format parsed analysis data as markdown with tables for key issues."""
        md_output = []

        # Extract the review data (it's nested under 'review' key)
        review_data = analysis_data.get('review', analysis_data)

        # Title
        md_output.append("# Code Review Analysis")
        md_output.append("")

        # Overall metrics
        score = review_data.get('score')
        effort = review_data.get('estimated_effort_to_review')

        if score is not None or effort is not None:
            md_output.append("## Review Metrics")
            if score is not None:
                # Add visual indicator for score
                if score >= 80:
                    score_indicator = "🟢"
                elif score >= 60:
                    score_indicator = "🟡"
                else:
                    score_indicator = "🔴"
                md_output.append(f"**Code Quality Score:** {score_indicator} {score}/100")

            if effort is not None:
                # Add visual indicator for effort
                effort_indicators = ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]
                effort_indicator = effort_indicators[min(effort - 1, 4)] if effort > 0 else ""
                md_output.append(f"**Review Effort:** {effort_indicator} {effort}/5")

            md_output.append("")

        # TODO sections
        todo_sections = review_data.get('todo_sections')
        if todo_sections and todo_sections != "No":
            md_output.append("## TODO Items")
            if isinstance(todo_sections, list):
                for todo in todo_sections:
                    if isinstance(todo, dict):
                        file_name = todo.get('file', 'Unknown file')
                        content = todo.get('content', 'No content')
                        line = todo.get('line', 'Unknown line')
                        md_output.append(f"- **{file_name}:{line}** - {content}")
                    else:
                        md_output.append(f"- {todo}")
            else:
                md_output.append(str(todo_sections))
            md_output.append("")

        # Key issues table
        key_issues = review_data.get('key_issues_to_review', [])
        if key_issues:
            md_output.append("## Key Issues to Review")
            md_output.append("")

            # Create markdown table
            md_output.append("| File | Issue | Lines | Description |")
            md_output.append("|------|-------|-------|-------------|")

            for issue in key_issues:
                file_name = issue.get('relevant_file', 'Unknown')
                issue_header = issue.get('issue_header', 'No header')
                issue_content = issue.get('issue_content', 'No content')
                start_line = issue.get('start_line', '')
                end_line = issue.get('end_line', '')

                # Escape pipe characters in content
                file_escaped = file_name.replace('|', '\\|')
                header_escaped = issue_header.replace('|', '\\|')
                content_escaped = issue_content.replace('|', '\\|').replace('\n', '<br>')

                # Format line range
                if start_line and end_line:
                    if start_line == end_line:
                        line_range = str(start_line)
                    else:
                        line_range = f"{start_line}-{end_line}"
                elif start_line:
                    line_range = str(start_line)
                elif end_line:
                    line_range = str(end_line)
                else:
                    line_range = "N/A"

                md_output.append(f"| `{file_escaped}` | **{header_escaped}** | `{line_range}` | {content_escaped} |")

            md_output.append("")

        return "\n".join(md_output)

    def _format_comment_markdown(self, comment_data: Dict[str, Any]) -> str:
        """Format parsed comment data as markdown with tables for code suggestions."""
        md_output = []

        # Title
        md_output.append("# Code Suggestions Review")
        md_output.append("")

        # Extract code suggestions
        code_suggestions = comment_data.get('code_suggestions', [])

        if not code_suggestions:
            md_output.append("No code suggestions found.")
            return "\n".join(md_output)

        # Summary statistics
        total_suggestions = len(code_suggestions)

        # Group suggestions by label for better organization
        label_groups = {}
        for suggestion in code_suggestions:
            label = suggestion.get('label', 'other')
            if label not in label_groups:
                label_groups[label] = []
            label_groups[label].append(suggestion)

        md_output.append("## Summary")
        md_output.append(f"**Total Suggestions:** {total_suggestions}")

        # Show breakdown by label
        for label, suggestions in sorted(label_groups.items()):
            count = len(suggestions)
            # Add emoji indicators for different types
            if label in ['security', 'possible bug']:
                emoji = "🔴"
            elif label in ['possible issue', 'performance']:
                emoji = "🟡"
            elif label in ['enhancement', 'best practice', 'maintainability']:
                emoji = "🟢"
            elif label == 'typo':
                emoji = "✏️"
            else:
                emoji = "📝"
            md_output.append(f"**{label.title()}:** {emoji} {count}")
        md_output.append("")

        # Group suggestions by priority based on label
        critical_labels = ['security', 'possible bug']
        important_labels = ['possible issue', 'performance']
        improvement_labels = ['enhancement', 'best practice', 'maintainability']
        minor_labels = ['typo']

        critical_suggestions = [s for s in code_suggestions if s.get('label', 'other') in critical_labels]
        important_suggestions = [s for s in code_suggestions if s.get('label', 'other') in important_labels]
        improvement_suggestions = [s for s in code_suggestions if s.get('label', 'other') in improvement_labels]
        minor_suggestions = [s for s in code_suggestions if s.get('label', 'other') in minor_labels]
        other_suggestions = [s for s in code_suggestions if s.get('label', 'other') not in critical_labels + important_labels + improvement_labels + minor_labels]

        # Critical suggestions
        if critical_suggestions:
            md_output.append("## 🔴 Critical Issues")
            md_output.append("")
            self._add_suggestions_table(md_output, critical_suggestions)
            md_output.append("")

        # Important suggestions
        if important_suggestions:
            md_output.append("## 🟡 Important Issues")
            md_output.append("")
            self._add_suggestions_table(md_output, important_suggestions)
            md_output.append("")

        # Improvement suggestions
        if improvement_suggestions:
            md_output.append("## 🟢 Code Improvements")
            md_output.append("")
            self._add_suggestions_table(md_output, improvement_suggestions)
            md_output.append("")

        # Minor suggestions
        if minor_suggestions:
            md_output.append("## ✏️ Minor Issues")
            md_output.append("")
            self._add_suggestions_table(md_output, minor_suggestions)
            md_output.append("")

        # Other suggestions
        if other_suggestions:
            md_output.append("## 📝 Other Suggestions")
            md_output.append("")
            self._add_suggestions_table(md_output, other_suggestions)
            md_output.append("")

        return "\n".join(md_output)

    def _add_suggestions_table(self, md_output: List[str], suggestions: List[Dict[str, Any]]):
        """Add a markdown table for a list of suggestions."""
        for i, suggestion in enumerate(suggestions, 1):
            file_name = suggestion.get('relevant_file', 'Unknown')
            language = suggestion.get('language', 'unknown')
            line_number = suggestion.get('line_number', '')
            suggestion_content = suggestion.get('suggestion_content', 'No suggestion')
            improved_code = suggestion.get('improved_code', '')
            one_sentence_summary = suggestion.get('one_sentence_summary', 'No summary')
            label = suggestion.get('label', 'other')

            # Escape pipe characters and format content for markdown
            file_escaped = file_name.replace('|', '\\|')
            suggestion_content_escaped = suggestion_content.replace('|', '\\|').replace('\n', '<br>')
            one_sentence_summary_escaped = one_sentence_summary.replace('|', '\\|')

            # Format improved code for display (truncate if too long)
            improved_code_display = improved_code.replace('|', '\\|').replace('\n', '<br>')
            if len(improved_code_display) > 100:
                improved_code_display = improved_code_display[:97] + "..."

            # Add label indicator
            if label in ['security', 'possible bug']:
                label_display = f"🔴 {label}"
            elif label in ['possible issue', 'performance']:
                label_display = f"🟡 {label}"
            elif label in ['enhancement', 'best practice', 'maintainability']:
                label_display = f"🟢 {label}"
            elif label == 'typo':
                label_display = f"✏️ {label}"
            else:
                label_display = f"📝 {label}"

            # Create individual suggestion section
            md_output.append(f"### {i}. {one_sentence_summary_escaped}")
            md_output.append("")
            md_output.append(f"**File:** `{file_escaped}` ({language})")
            if line_number:
                md_output.append(f"**Line:** {line_number}")
            md_output.append(f"**Label:** {label_display}")
            md_output.append("")
            md_output.append(f"**Suggestion:** {suggestion_content_escaped}")
            md_output.append("")

            if improved_code.strip():
                md_output.append("**Improved Code:**")
                md_output.append("```" + language)
                md_output.append(improved_code)
                md_output.append("```")
                md_output.append("")

            md_output.append("---")
            md_output.append("")

    def _format_thinking_section(self, thinking: str, phase_name: str) -> str:
        """Format thinking content in a collapsible markdown section.

        Args:
            thinking: The thinking content from the model
            phase_name: Name of the phase for the section title

        Returns:
            Formatted markdown with collapsible thinking section
        """
        if not thinking or not thinking.strip():
            return ""

        # Clean up the thinking content
        thinking_clean = thinking.strip()

        # Create collapsible section using HTML details/summary
        thinking_section = f"""
<details>
<summary><strong>🧠 Model Thinking - {phase_name}</strong> <em>(Click to expand)</em></summary>

```
{thinking_clean}
```

</details>"""

        return thinking_section

    def _format_list_to_markdown(self, content: Union[str, List[str]]) -> str:
        """Format a list into a markdown string, otherwise return the content as a string."""
        if isinstance(content, list):
            return "\n".join(f"- {item}" for item in content)
        return str(content)