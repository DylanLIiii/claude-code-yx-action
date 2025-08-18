"""Module for reading markdown files as system and user prompts."""

from pathlib import Path
from typing import Dict, Optional


class PromptReader:
    """Reads markdown files from directories to use as prompts."""
    
    def __init__(self, prompts_dir: Path):
        """Initialize with directory containing prompt files."""
        self.prompts_dir = Path(prompts_dir)
        if not self.prompts_dir.exists():
            raise ValueError(f"Prompts directory does not exist: {prompts_dir}")
    
    def read_system_prompt(self, stage: str) -> str:
        """Read system prompt for a specific review stage."""
        prompt_file = self.prompts_dir / f"{stage}.md"
        if not prompt_file.exists():
            raise FileNotFoundError(f"System prompt file not found: {prompt_file}")
        
        return prompt_file.read_text(encoding='utf-8').strip()
    
    def read_all_prompts(self) -> Dict[str, str]:
        """Read all available prompt files."""
        prompts = {}
        for prompt_file in self.prompts_dir.glob("*.md"):
            stage_name = prompt_file.stem
            prompts[stage_name] = prompt_file.read_text(encoding='utf-8').strip()
        return prompts
    
    def validate_prompts_exist(self, required_stages: list[str]) -> bool:
        """Check if all required prompt files exist."""
        for stage in required_stages:
            prompt_file = self.prompts_dir / f"{stage}.md"
            if not prompt_file.exists():
                return False
        return True