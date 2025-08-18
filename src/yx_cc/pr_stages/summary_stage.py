"""Stage 1: PR Summary Generation."""

from typing import Dict, Any
from ..core.prompt_reader import PromptReader
from ..integrations.ali_yunxiao import AliYunXiaoClient


class SummaryStage:
    """First stage: Generate PR description and summary."""
    
    def __init__(self, prompt_reader: PromptReader, ai_client: AliYunXiaoClient):
        """Initialize summary stage with prompt reader and AI client."""
        self.prompt_reader = prompt_reader
        self.ai_client = ai_client
    
    def generate_summary(self, commit_info: Dict[str, Any], diff_content: str) -> str:
        """Generate PR summary using predefined system prompt."""
        try:
            # Read system prompt for summary stage
            system_prompt = self.prompt_reader.read_system_prompt('summary')
            
            # Generate summary using AI client
            summary = self.ai_client.generate_summary(
                system_prompt=system_prompt,
                commit_info=commit_info,
                diff_content=diff_content
            )
            
            return summary
            
        except Exception as e:
            return f"Error generating summary: {str(e)}"