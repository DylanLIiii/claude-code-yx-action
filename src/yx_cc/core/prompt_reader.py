"""Module for reading TOML files as system and user prompts."""

from pathlib import Path
from typing import Dict, Optional
import tomli
from loguru import logger
from .utils import num_tokens_from_string


class PromptReader:
    """Reads TOML files from directories to use as prompts."""
    
    def __init__(self, prompts_dir: Path):
        """Initialize with directory containing prompt files."""
        self.prompts_dir = Path(prompts_dir)
        if not self.prompts_dir.exists():
            raise ValueError(f"Prompts directory does not exist: {prompts_dir}")
        
        # Cache for REVIEW.md content to avoid reading multiple times
        self._review_md_content = None
        self._review_md_checked = False
    
    def _find_and_read_review_md(self) -> Optional[str]:
        """Find and read REVIEW.md from current directory or home directory."""
        if self._review_md_checked:
            return self._review_md_content
        
        self._review_md_checked = True
        
        # Define search locations in priority order
        search_paths = [
            Path.cwd() / "REVIEW.md",          # Current working directory
            Path.home() / "REVIEW.md"          # Home directory
        ]
        
        for review_path in search_paths:
            if review_path.exists() and review_path.is_file():
                try:
                    # Read the file with multiple encoding attempts
                    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
                    content = None
                    
                    for encoding in encodings:
                        try:
                            content = review_path.read_text(encoding=encoding)
                            break
                        except UnicodeDecodeError:
                            continue
                    
                    if content is None:
                        # Fallback to binary read with error handling
                        content = review_path.read_bytes().decode('utf-8', errors='replace')
                    
                    # Check token count
                    token_count = num_tokens_from_string(content)
                    max_tokens = 10000
                    
                    if token_count > max_tokens:
                        logger.warning(
                            f"REVIEW.md exceeds {max_tokens} tokens ({token_count} tokens). "
                            f"Content will be truncated. Found at: {review_path}"
                        )
                        # Truncate content using actual chars-per-token ratio
                        chars_per_token = len(content) / token_count if token_count else 4
                        estimated_max_chars = int(max_tokens * chars_per_token)
                        marker = "\n\n[... content truncated due to token limit ...]"
                        
                        if estimated_max_chars < 0:
                            estimated_max_chars = 0
                        
                        truncated_main = content[:estimated_max_chars]
                        content = truncated_main + marker
                        
                        # Refine truncation if we still exceed token limit (iterative adjustment)
                        for _ in range(5):
                            current_tokens = num_tokens_from_string(content)
                            if current_tokens <= max_tokens:
                                break
                            # Scale down proportionally
                            allowed_fraction = max_tokens / current_tokens
                            new_main_len = int(len(truncated_main) * allowed_fraction)
                            if new_main_len <= 0:
                                truncated_main = ""
                            else:
                                truncated_main = truncated_main[:new_main_len]
                            content = truncated_main + marker
                        
                        # Verify truncated content is within limits
                        truncated_tokens = num_tokens_from_string(content)
                        logger.info(f"Truncated REVIEW.md to {truncated_tokens} tokens")
                    else:
                        logger.info(f"Found REVIEW.md with {token_count} tokens at: {review_path}")
                    
                    self._review_md_content = content
                    return content
                    
                except Exception as e:
                    logger.warning(f"Failed to read REVIEW.md from {review_path}: {e}")
                    continue
        
        logger.debug("No REVIEW.md file found in current directory or home directory")
        return None
    
    def read_system_prompt(self, stage: str) -> str:
        """Read system prompt for a specific review stage."""
        prompt_file = self.prompts_dir / f"{stage}.toml"
        if not prompt_file.exists():
            raise FileNotFoundError(f"System prompt file not found: {prompt_file}")

        # Try different encodings to handle various file formats
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']

        for encoding in encodings:
            try:
                content = prompt_file.read_text(encoding=encoding)
                toml_data = tomli.loads(content)
                if 'prompt' in toml_data and 'system_prompt' in toml_data['prompt']:
                    system_prompt = toml_data['prompt']['system_prompt'].strip()
                    
                    # Append REVIEW.md content for stage 2 and 3
                    if stage in ['2', 'stage2', 'analysis', '3', 'stage3', 'comments']:
                        review_content = self._find_and_read_review_md()
                        if review_content:
                            system_prompt += f"\n\n## Additional Review Guidelines (from REVIEW.md)\n\n{review_content}"
                            logger.debug(f"Appended REVIEW.md content to {stage} system prompt")
                    
                    return system_prompt
                else:
                    raise ValueError(f"Invalid TOML format in {prompt_file}: missing 'prompt.system_prompt' section")
            except UnicodeDecodeError:
                continue
            except Exception as e:
                raise ValueError(f"Failed to parse TOML file {prompt_file}: {e}")

        # If all encodings fail, read as binary and decode with error handling
        try:
            content = prompt_file.read_bytes()
            decoded_content = content.decode('utf-8', errors='replace')
            toml_data = tomli.loads(decoded_content)
            if 'prompt' in toml_data and 'system_prompt' in toml_data['prompt']:
                system_prompt = toml_data['prompt']['system_prompt'].strip()
                
                # Append REVIEW.md content for stage 2 and 3
                if stage in ['2', 'stage2', 'analysis', '3', 'stage3', 'comments']:
                    review_content = self._find_and_read_review_md()
                    if review_content:
                        system_prompt += f"\n\n## Additional Review Guidelines (from REVIEW.md)\n\n{review_content}"
                        logger.debug(f"Appended REVIEW.md content to {stage} system prompt")
                
                return system_prompt
            else:
                raise ValueError(f"Invalid TOML format in {prompt_file}: missing 'prompt.system_prompt' section")
        except Exception as e:
            raise ValueError(f"Failed to read and parse TOML file {prompt_file}: {e}")
    
    def read_all_prompts(self) -> Dict[str, str]:
        """Read all available prompt files."""
        prompts = {}
        for prompt_file in self.prompts_dir.glob("*.toml"):
            stage_name = prompt_file.stem
            try:
                # Use the same encoding handling as read_system_prompt
                encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']

                content = None
                for encoding in encodings:
                    try:
                        content = prompt_file.read_text(encoding=encoding)
                        break
                    except UnicodeDecodeError:
                        continue

                if content is None:
                    # Fallback to binary read with error handling
                    content = prompt_file.read_bytes().decode('utf-8', errors='replace')

                toml_data = tomli.loads(content)
                if 'prompt' in toml_data and 'system_prompt' in toml_data['prompt']:
                    system_prompt = toml_data['prompt']['system_prompt'].strip()
                    
                    # Append REVIEW.md content for stage 2 and 3
                    if stage_name in ['2', 'stage2', 'analysis', '3', 'stage3', 'comments']:
                        review_content = self._find_and_read_review_md()
                        if review_content:
                            system_prompt += f"\n\n## Additional Review Guidelines (from REVIEW.md)\n\n{review_content}"
                            logger.debug(f"Appended REVIEW.md content to {stage_name} system prompt")
                    
                    prompts[stage_name] = system_prompt
                else:
                    raise ValueError(f"Invalid TOML format in {prompt_file}: missing 'prompt.system_prompt' section")

            except Exception as e:
                print(f"Warning: Failed to read prompt file {prompt_file}: {e}")
                prompts[stage_name] = f"Error reading prompt file: {e}"

        return prompts
    
    def clear_review_cache(self) -> None:
        """Clear the cached REVIEW.md content to force re-reading."""
        self._review_md_content = None
        self._review_md_checked = False
        logger.debug("Cleared REVIEW.md cache")
    
    def validate_prompts_exist(self, required_stages: list[str]) -> bool:
        """Check if all required prompt files exist."""
        for stage in required_stages:
            prompt_file = self.prompts_dir / f"{stage}.toml"
            if not prompt_file.exists():
                return False
        return True