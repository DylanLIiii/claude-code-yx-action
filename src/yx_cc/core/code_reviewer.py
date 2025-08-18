"""Main code review engine orchestrating the multi-stage review process."""

from pathlib import Path
from typing import Dict, Any

from .prompt_reader import PromptReader
from .output_formatter import OutputFormatter, ReviewResult
from ..integrations.git_handler import GitHandler
from ..integrations.ali_yunxiao import AliYunXiaoClient
from ..pr_stages.summary_stage import SummaryStage
from ..pr_stages.analysis_stage import AnalysisStage
from ..pr_stages.comment_stage import CommentStage


class CodeReviewer:
    """Main orchestrator for multi-stage code review process."""
    
    def __init__(self, prompts_dir: Path, output_format: str = 'markdown'):
        """Initialize code reviewer with configuration."""
        self.prompt_reader = PromptReader(prompts_dir)
        self.output_formatter = OutputFormatter(output_format)
        self.git_handler = GitHandler()
        self.ai_client = AliYunXiaoClient()
        
        # Validate required prompts exist
        required_stages = ['summary', 'analysis', 'comment']
        if not self.prompt_reader.validate_prompts_exist(required_stages):
            raise ValueError("Missing required system prompt files")
        
        # Initialize review stages
        self.summary_stage = SummaryStage(self.prompt_reader, self.ai_client)
        self.analysis_stage = AnalysisStage(self.prompt_reader, self.ai_client)
        self.comment_stage = CommentStage(self.prompt_reader, self.ai_client)
    
    def review_commit(self, commit_id: str) -> str:
        """Execute full multi-stage code review process."""
        # Get commit information and diff
        commit_info = self.git_handler.get_commit_info(commit_id)
        diff_content = self.git_handler.get_commit_diff(commit_id)
        
        # Stage 1: Generate summary
        summary = self.summary_stage.generate_summary(commit_info, diff_content)
        
        # Stage 2: Analyze changes
        analysis = self.analysis_stage.analyze_changes(commit_info, diff_content, summary)
        
        # Stage 3: Generate patch comments
        comments = self.comment_stage.generate_comments(commit_info, diff_content, analysis)
        
        # Prepare metadata
        metadata = {
            'review_timestamp': self.git_handler.get_current_timestamp(),
            'commit_author': commit_info.get('author', 'Unknown'),
            'commit_date': commit_info.get('date', 'Unknown'),
            'files_changed': len(commit_info.get('files', [])),
            'total_comments': len(comments)
        }
        
        # Create result object
        result = ReviewResult(
            commit_id=commit_id,
            summary=summary,
            analysis=analysis,
            comments=comments,
            metadata=metadata
        )
        
        # Format and return result
        return self.output_formatter.format_result(result)