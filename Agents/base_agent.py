# pylint: disable=import-error
"BaseAgent"
from typing import Optional
from langchain_anthropic import ChatAnthropic
from langchain_aws import ChatBedrock
from langchain_openai import ChatOpenAI
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Settings


class BaseAgent:
    """Base agent class for handling LLM interactions"""

    def __init__(self, settings: Settings):
        """Initialize BaseAgent with settings

        Args:
            settings (Settings): Application settings instance
            containing API keys and configurations
        """
        self.settings = settings

        # Initialize Claude
        self.claude = self._initialize_claude()

        # Initialize GPT-4
        self.gpt4 = self._initialize_gpt4()

    def _initialize_claude(self) -> Optional[ChatAnthropic]:
        """Initialize Claude model with proper error handling

        Returns:
            ChatAnthropic: Initialized Claude model instance
            None: If initialization fails
        """
        try:
            return ChatBedrock(
                model_id=self.settings.CLAUDE_API_KEY,
                model_kwargs=dict(temperature=0),
                aws_access_key_id=self.settings.ACCESS_KEY_ID,
                aws_secret_access_key=self.settings.SECRET_ACCESS_KEY,
                region_name="eu-west-3",
            )
        except Exception as e:
            if self.settings.is_production:
                raise Exception("Failed to initialize Claude model") from e
            print(f"Warning: Failed to initialize Claude model: {str(e)}")
            return None

    def _initialize_gpt4(self) -> Optional[ChatOpenAI]:
        """Initialize GPT-4 model with proper error handling

        Returns:
            ChatOpenAI: Initialized GPT-4 model instance
            None: If initialization fails
        """
        try:
            return ChatOpenAI(
                api_key=self.settings.OPENAI_API_KEY,
                model=self.settings.GPT4_MODEL,
                temperature=0.5,
                max_retries=3,
                request_timeout=300,  # 5 minutes timeout
            )
        except Exception as e:
            if self.settings.is_production:
                raise Exception("Failed to initialize GPT-4 model") from e
            print(f"Warning: Failed to initialize GPT-4 model: {str(e)}")
            return None

    def get_available_models(self) -> list[str]:
        """Get list of available LLM models

        Returns:
            list[str]: List of available model names
        """
        models = []
        if self.claude:
            models.append("claude")
        if self.gpt4:
            models.append("gpt4")
        return models
