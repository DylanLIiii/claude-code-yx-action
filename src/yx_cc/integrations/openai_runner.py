"""Simple, flexible interface for OpenAI API operations."""

import os
import asyncio
from typing import Optional, Dict, Any, Literal
from loguru import logger
from ..core.utils import num_tokens_from_string, JsonDumper

try:
    from openai import AsyncOpenAI
except ImportError:
    raise ImportError(
        "OpenAI library not found. Please install it with: pip install openai"
    )


class OpenAIRunner:
    """Simple, flexible interface for OpenAI API operations."""

    def __init__(self, max_turns: int = 2, temperature: float = 0.8):
        """Initialize with default options."""
        self.model = os.getenv('OPENAI_MODEL')
        # TODO: fix turns
        self.max_turns = 1
        self.temperature = temperature
        self.max_tokens = 50000

        # Get OpenAI configuration from environment
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.base_url = os.getenv('OPENAI_BASE_URL')
        
        logger.info(f"Initializing OpenAI runner with model={self.model}, max_turns={max_turns}, temperature={temperature}")
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        logger.debug(f"Using OpenAI base URL: {self.base_url or 'default'}")

        # Initialize OpenAI client
        client_kwargs = {"api_key": self.api_key}
        if self.base_url:
            client_kwargs["base_url"] = self.base_url
            
        self.client = AsyncOpenAI(**client_kwargs)

        # Initialize JSON dumper for storing OpenAI responses
        self.json_dumper = JsonDumper()
        logger.debug("JSON dumper initialized for OpenAI runner")

    def run(self, system_prompt: str, prompt: str, max_turns: Optional[int] = None) -> str:
        """Run a synchronous OpenAI API call."""
        return asyncio.run(self.run_async(system_prompt, prompt, max_turns))

    async def run_async(self, system_prompt: str, prompt: str, max_turns: Optional[int] = None) -> str:
        """Run an asynchronous OpenAI API call."""
        
        num_system_prompt_tokens = num_tokens_from_string(system_prompt)
        num_user_prompt_tokens = num_tokens_from_string(prompt)

        logger.debug(f"System prompt length: {num_system_prompt_tokens} tokens")
        logger.debug(f"User prompt length: {num_user_prompt_tokens} tokens")
        
        # Limit prompt length under 50K tokens
        if num_system_prompt_tokens + num_user_prompt_tokens > self.max_tokens: 
            raise ValueError(f"Combined prompt length exceeds maximum limit of {self.max_tokens} tokens, current token length is {num_system_prompt_tokens + num_user_prompt_tokens}")

        try:
            # Prepare messages for conversation
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]

            logger.debug("OpenAI client initialized, sending query")

            response_chunks = []
            
                
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                stream=False  # For simplicity, not streaming initially
            )
            
            if response.choices and response.choices[0].message.content:
                content = response.choices[0].message.content
                response_chunks.append(content)
                
                # Add assistant response to conversation for potential next turn
                messages.append({"role": "assistant", "content": content})

            else:
                logger.warning(f"No content received in turn {turn + 1}")

            result = ''.join(response_chunks).strip()
            logger.info(f"OpenAI API call completed successfully, response length: {len(result)} characters")

            # Dump OpenAI response to JSON file
            try:
                openai_data = {
                    'system_prompt': system_prompt[:500] + "..." if len(system_prompt) > 500 else system_prompt,
                    'user_prompt': prompt[:500] + "..." if len(prompt) > 500 else prompt,
                    'model': self.model,
                    'temperature': self.temperature,
                    'response': result,
                    'response_length': len(result),
                    'turns_used': len(response_chunks)
                }
                json_file_path = self.json_dumper.dump_results("openai_response", openai_data)
                logger.debug(f"OpenAI response dumped to: {json_file_path}")
            except Exception as dump_error:
                logger.error(f"Failed to dump OpenAI response to JSON: {dump_error}")

            return result

        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
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
