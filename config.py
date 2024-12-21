"Config"
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    CLAUDE_MODEL = os.getenv("OPENAI_API_KEY")
    GPT4_MODEL = "gpt-4-turbo-preview"
    ANTHROPIC_API_KEY = os.getenv("INFERENCE_PROFILE_ID")