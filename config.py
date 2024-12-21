"Config class"
from functools import lru_cache
import os
from typing import Optional
from dotenv import load_dotenv

# Only load .env file if it exists
if os.path.exists(".env"):
    load_dotenv()
    print("Loaded environment variables from .env file")


class Settings:
    """Configuration settings for the application."""
    def __init__(self, env_file: Optional[str] = None):
        # API Keys and Credentials
        self.OPENAI_API_KEY: str = self._get_required_env("OPENAI_API_KEY")
        self.CLAUDE_API_KEY: str = self._get_required_env("INFERENCE_PROFILE_ID")
        self.ACCESS_KEY_ID: str = self._get_required_env("ACCESS_KEY_ID")
        self.SECRET_ACCESS_KEY: str = self._get_required_env("SECRET_ACCESS_KEY")
        
        # Constants
        self.GPT4_MODEL: str = "GPT-4o"
        
        # Environment
        self.ENVIRONMENT: str = os.getenv("ENVIRONMENT", "local")
        
        # Optional: Load from env file if specified
        if env_file and os.path.exists(env_file):
            load_dotenv(env_file)

    def _get_required_env(self, key: str) -> str:
        """Get a required environment variable or raise an error."""
        value = os.getenv(key)
        if value is None:
            raise ValueError(f"Missing required environment variable: {key}")
        return value

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT.lower() in ("production", "prod", "server")


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance based on environment."""
    environment = os.getenv("ENVIRONMENT", "local").lower()
    
    if environment == "local":
        return Settings(env_file=".env")
    elif environment in ("production", "prod", "server"):
        return Settings()
    else:
        raise ValueError(f"Invalid environment: {environment}")
