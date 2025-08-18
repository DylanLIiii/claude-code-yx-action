"""Simple, flexible interface for Claude Code SDK operations."""

from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions
import asyncio
from typing import Optional, Dict, Any, Literal
from loguru import logger


class ClaudeCodeRunner:
    """Simple, flexible interface for Claude Code SDK operations."""

    def __init__(self, permission_mode: Literal['default', 'acceptEdits', 'plan', 'bypassPermissions'] = 'plan', max_turns: int = 2):
        """Initialize with default options."""
        logger.info(f"Initializing Claude Code runner with permission_mode={permission_mode}, max_turns={max_turns}")
        self.permission_mode = permission_mode
        self.max_turns = max_turns

    def run(self, system_prompt: str, prompt: str, max_turns: Optional[int] = None) -> str:
        """Run a synchronous Claude Code SDK call."""
        return asyncio.run(self.run_async(system_prompt, prompt, max_turns))

    async def run_async(self, system_prompt: str, prompt: str, max_turns: Optional[int] = None) -> str:
        """Run an asynchronous Claude Code SDK call."""
        turns = max_turns if max_turns is not None else self.max_turns

        logger.debug(f"Starting Claude Code SDK call with max_turns={turns}")
        logger.debug(f"System prompt length: {len(system_prompt)} characters")
        logger.debug(f"User prompt length: {len(prompt)} characters")

        try:
            async with ClaudeSDKClient(
                options=ClaudeCodeOptions(
                    system_prompt=system_prompt,
                    permission_mode=self.permission_mode,
                    max_turns=turns,
                )
            ) as client:
                logger.debug("Claude SDK client initialized, sending query")
                await client.query(prompt)

                chunks = []
                message_count = 0

                logger.debug("Receiving response from Claude SDK")
                async for message in client.receive_response():
                    message_count += 1
                    logger.debug(f"Received message {message_count}")

                    if hasattr(message, 'content'):
                        for block in getattr(message, 'content', []) or []:
                            if hasattr(block, 'text') and isinstance(block.text, str):
                                chunks.append(block.text)

                result = ''.join(chunks).strip()
                logger.info(f"Claude SDK call completed successfully, response length: {len(result)} characters")
                return result

        except Exception as e:
            logger.error(f"Claude Code SDK call failed: {e}")
            raise

    def run_with_context(self, system_prompt: str, prompt: str, context: Dict[str, Any], max_turns: Optional[int] = None) -> str:
        """Run with additional context information."""
        enhanced_prompt = self._build_prompt_with_context(prompt, context)
        return self.run(system_prompt, enhanced_prompt, max_turns)

    def _build_prompt_with_context(self, prompt: str, context: Dict[str, Any]) -> str:
        """Build prompt with context information."""
        context_lines = []
        for key, value in context.items():
            if isinstance(value, str):
                context_lines.append(f"{key}: {value}")
            elif isinstance(value, (list, dict)):
                context_lines.append(f"{key}: {str(value)}")

        if context_lines:
            context_section = "\n".join(context_lines)
            return f"Context:\n{context_section}\n\n{prompt}"
        return prompt


# Backward compatibility - keep the old interface
class _ClaudeRunner:
    """Internal helper to run Claude Code SDK calls synchronously."""

    @staticmethod
    def run(system_prompt: str, prompt: str, max_turns: int = 2) -> str:
        runner = ClaudeCodeRunner(max_turns=max_turns)
        return runner.run(system_prompt, prompt)