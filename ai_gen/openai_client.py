"""
OpenAI API integration and client setup.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI Model Configuration
OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_DEFAULT_TEMPERATURE = 0.4
OPENAI_DEFAULT_MAX_TOKENS = 1000


class OpenAIClient:
    """Client for interacting with OpenAI API."""
    
    def __init__(self, api_key=None):
        """
        Initialize OpenAI client.
        
        Args:
            api_key: Optional API key. If not provided, uses OPENAI_API_KEY from config.
        """
        self.api_key = api_key or OPENAI_API_KEY
        if not self.api_key:
            raise RuntimeError("OpenAI API key not found! Please set OPENAI_API_KEY in .env file.")
        self.client = OpenAI(api_key=self.api_key)
    
    def call_openai(self, prompt, max_tokens=None, temperature=None):
        """
        Call OpenAI API with a prompt.
        
        Args:
            prompt: The prompt text to send to the model
            max_tokens: Maximum tokens in response (defaults to config value)
            temperature: Temperature setting (defaults to config value)
        
        Returns:
            str: The model's response content
        """
        if self.client is None:
            raise RuntimeError("OpenAI client is not configured. Add OPENAI_API_KEY.")
        
        response = self.client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature if temperature is not None else OPENAI_DEFAULT_TEMPERATURE,
            max_tokens=max_tokens if max_tokens is not None else OPENAI_DEFAULT_MAX_TOKENS
        )
        return str(response.choices[0].message.content)

