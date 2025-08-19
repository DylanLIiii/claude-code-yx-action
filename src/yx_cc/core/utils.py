import tiktoken
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

def num_tokens_from_string(text: str, model_name: str = "gpt-4o") -> int:
    """Return number of tokens in a text string for a specified model."""
    encoding = tiktoken.encoding_for_model(model_name)
    tokens = encoding.encode(text)
    return len(tokens)


def split_thinking_and_json(content: str) -> tuple[str, str]:
    """
    Split a combined model output into (thinking, raw_json_string).

    Looks for the first ```json fence (case-insensitive). Everything before it
    is 'thinking'. Then captures everything until the next ``` fence. If no
    closing fence exists, it returns everything after ```json exactly (trimmed
    on the left where the JSON normally starts).

    Args:
        content: Full model output.

    Returns:
        thinking: Text before the first ```json fence (stripped).
        raw_json_string: Raw JSON substring (stripped) if a fence was found,
                         else None. If the fence is present but empty, returns content originally.
                         If no closing fence, returns the remainder after ```json.
    """
    fence_marker = "```json"
    lower_content = content.lower()
    idx = lower_content.find(fence_marker)
    if idx == -1:
        return content.strip(), None

    thinking = content[:idx].strip()
    remainder = content[idx + len(fence_marker):].lstrip()

    end_idx = remainder.find("```")
    if end_idx == -1:
        # No closing fence: return everything after ```json (strip to be consistent)
        json_block = remainder.strip()
    else:
        json_block = remainder[:end_idx].strip()

    if not json_block:
        return thinking, content
    return thinking, json_block


def safe_json_repair(json_str: str) -> str:
    """Repair JSON while preserving Chinese characters.
    
    This function wraps json_repair but ensures Chinese characters
    are not escaped as Unicode sequences.
    
    Args:
        json_str: JSON string to repair
        
    Returns:
        Repaired JSON string with proper Chinese character display
    """
    try:
        from json_repair import repair_json
        repaired = repair_json(json_str)
        
        # Parse and re-serialize with ensure_ascii=False to preserve Chinese characters
        import json
        parsed = json.loads(repaired)
        return json.dumps(parsed, ensure_ascii=False, indent=2)
    except Exception:
        # If repair fails, just return the original string
        return json_str


def safe_json_dumps(obj: Any, **kwargs) -> str:
    """JSON dumps with Chinese character support by default.
    
    This function ensures Chinese characters are not escaped as Unicode sequences.
    
    Args:
        obj: Object to serialize
        **kwargs: Additional arguments for json.dumps
    
    Returns:
        JSON string with proper Chinese character display
    """
    # Always ensure Chinese characters are not escaped
    kwargs.setdefault('ensure_ascii', False)
    # Default to pretty formatting
    kwargs.setdefault('indent', 2)
    return json.dumps(obj, **kwargs)


class JsonDumper:
    """Simple JSON dump utility for storing results with timestamps."""

    def __init__(self, base_dir: Optional[str] = None):
        """Initialize JsonDumper with base directory.

        Args:
            base_dir: Base directory for storing JSON files. Defaults to ./tmp
        """
        if base_dir is None:
            base_dir = "./tmp"
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)

    def create_empty_json(self, filename: str) -> Path:
        """Create an empty JSON file with timestamp.

        Args:
            filename: Base filename (without extension)

        Returns:
            Path to the created file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        full_filename = f"{filename}_{timestamp}.json"
        file_path = self.base_dir / full_filename

        # Create empty JSON structure
        empty_data = {
            "created_at": datetime.now().isoformat(),
            "filename": filename,
            "data": {}
        }

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(empty_data, f, indent=2, ensure_ascii=False)

        return file_path

    def dump_results(self, filename: str, data: Dict[str, Any]) -> Path:
        """Dump results to JSON file with timestamp.

        Args:
            filename: Base filename (without extension)
            data: Data to dump

        Returns:
            Path to the created file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        full_filename = f"{filename}_{timestamp}.json"
        file_path = self.base_dir / full_filename

        # Structure the data with metadata
        structured_data = {
            "created_at": datetime.now().isoformat(),
            "filename": filename,
            "data": data
        }

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(structured_data, f, indent=2, ensure_ascii=False)

        return file_path

    def append_to_json(self, file_path: Path, key: str, value: Any) -> None:
        """Append data to existing JSON file.

        Args:
            file_path: Path to existing JSON file
            key: Key to add/update
            value: Value to set
        """
        if not file_path.exists():
            raise FileNotFoundError(f"JSON file not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Update the data section
        data["data"][key] = value
        data["updated_at"] = datetime.now().isoformat()

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


