"""Stage 2: Change Analysis."""

from typing import Dict, Any
from ..core.prompt_reader import PromptReader
from ..integrations.ali_yunxiao import AliYunXiaoClient


class AnalysisStage:
    """Second stage: Analyze changes in the PR."""
    
    def __init__(self, prompt_reader: PromptReader, ai_client: AliYunXiaoClient):
        """Initialize analysis stage with prompt reader and AI client."""
        self.prompt_reader = prompt_reader
        self.ai_client = ai_client
    
    def analyze_changes(self, commit_info: Dict[str, Any], diff_content: str, summary: str) -> str:
        """Analyze PR changes using predefined system prompt."""
        try:
            # Read system prompt for analysis stage
            system_prompt = self.prompt_reader.read_system_prompt('analysis')
            
            # Analyze changes using AI client
            analysis = self.ai_client.analyze_changes(
                system_prompt=system_prompt,
                commit_info=commit_info,
                diff_content=diff_content,
                summary=summary
            )
            
            return analysis
            
        except Exception as e:
            return f"Error analyzing changes: {str(e)}"