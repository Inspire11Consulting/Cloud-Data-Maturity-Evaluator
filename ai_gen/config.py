"""
AI-related configuration for OpenAI integration.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI Model Configuration
OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_DEFAULT_TEMPERATURE = 0.4
OPENAI_DEFAULT_MAX_TOKENS = 1000

