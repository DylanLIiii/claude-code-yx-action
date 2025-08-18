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

        # Try different encodings to handle various file formats
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']

        for encoding in encodings:
            try:
                return prompt_file.read_text(encoding=encoding).strip()
            except UnicodeDecodeError:
                continue

        # If all encodings fail, read as binary and decode with error handling
        try:
            content = prompt_file.read_bytes()
            return content.decode('utf-8', errors='replace').strip()
        except Exception as e:
            raise ValueError(f"Failed to read prompt file {prompt_file}: {e}")
    
    def read_all_prompts(self) -> Dict[str, str]:
        """Read all available prompt files."""
        prompts = {}
        for prompt_file in self.prompts_dir.glob("*.md"):
            stage_name = prompt_file.stem
            try:
                # Use the same encoding handling as read_system_prompt
                encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']

                content = None
                for encoding in encodings:
                    try:
                        content = prompt_file.read_text(encoding=encoding).strip()
                        break
                    except UnicodeDecodeError:
                        continue

                if content is None:
                    # Fallback to binary read with error handling
                    content = prompt_file.read_bytes().decode('utf-8', errors='replace').strip()

                prompts[stage_name] = content
            except Exception as e:
                print(f"Warning: Failed to read prompt file {prompt_file}: {e}")
                prompts[stage_name] = f"Error reading prompt file: {e}"

        return prompts
    
    def validate_prompts_exist(self, required_stages: list[str]) -> bool:
        """Check if all required prompt files exist."""
        for stage in required_stages:
            prompt_file = self.prompts_dir / f"{stage}.md"
            if not prompt_file.exists():
                return False
        return True