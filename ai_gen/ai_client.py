"""
Anthropic API integration and client setup.
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Anthropic API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Anthropic Model Configuration
# Keep model configurable via env so different Anthropic accounts can use
# whichever model they have access to.
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
ANTHROPIC_DEFAULT_TEMPERATURE = 0.4
ANTHROPIC_DEFAULT_MAX_TOKENS = 1000


class AIClient:
    """Generic AI client currently backed by Anthropic."""
    
    def __init__(self, api_key=None):
        """
        Initialize Anthropic client.
        
        Args:
            api_key: Optional API key. If not provided, uses ANTHROPIC_API_KEY from config.
        """
        self.api_key = api_key or ANTHROPIC_API_KEY
        if not self.api_key:
            raise RuntimeError(
                "Anthropic API key not found! Please set ANTHROPIC_API_KEY in .env file."
            )
        self.client = Anthropic(api_key=self.api_key)
    
    def call_ai(self, prompt, max_tokens=None, temperature=None):
        """
        Call Anthropic API with a prompt.
        
        Args:
            prompt: The prompt text to send to the model
            max_tokens: Maximum tokens in response (defaults to config value)
            temperature: Temperature setting (defaults to config value)
        
        Returns:
            str: The model's response content
        """
        if self.client is None:
            raise RuntimeError("Anthropic client is not configured. Add ANTHROPIC_API_KEY.")

        response = self.client.messages.create(
            model=ANTHROPIC_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=(
                temperature if temperature is not None else ANTHROPIC_DEFAULT_TEMPERATURE
            ),
            max_tokens=max_tokens if max_tokens is not None else ANTHROPIC_DEFAULT_MAX_TOKENS,
        )

        if not response.content:
            return ""

        return "".join(
            block.text for block in response.content if getattr(block, "type", None) == "text"
        )

