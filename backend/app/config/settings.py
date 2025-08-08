"""Simple settings for hackathon MVP."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    api_title: str = "I-Fill-Forms API"
    api_version: str = "0.1.0"
    debug: bool = True
    
    # AI Settings (for OpenAI/Anthropic)
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    
    # CORS Settings
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()