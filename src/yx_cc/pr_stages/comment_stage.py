"""Stage 3: Patch Comment Generation."""

from typing import Dict, Any, List
from ..core.prompt_reader import PromptReader
from ..integrations.ali_yunxiao import AliYunXiaoClient


class CommentStage:
    """Third stage: Generate comments on patches that need attention."""
    
    def __init__(self, prompt_reader: PromptReader, ai_client: AliYunXiaoClient):
        """Initialize comment stage with prompt reader and AI client."""
        self.prompt_reader = prompt_reader
        self.ai_client = ai_client
    
    def generate_comments(self, commit_info: Dict[str, Any], 
                         diff_content: str, analysis: str) -> List[Dict[str, Any]]:
        """Generate patch comments using predefined system prompt."""
        try:
            # Read system prompt for comment stage
            system_prompt = self.prompt_reader.read_system_prompt('comment')
            
            # Generate comments using AI client
            comments = self.ai_client.generate_comments(
                system_prompt=system_prompt,
                commit_info=commit_info,
                diff_content=diff_content,
                analysis=analysis
            )
            
            return comments
            
        except Exception as e:
            return [{'file': 'Error', 'line': 'N/A', 'content': f"Error generating comments: {str(e)}"}]