"""Simple settings for hackathon MVP."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore"  # Ignore extra environment variables
    )
    
    # API Settings
    api_title: str = "I-Fill-Forms API"
    api_version: str = "0.1.0"
    debug: bool = True
    
    # AI Settings (for OpenAI/Anthropic)
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    
    # Groq API key for DSPy LLM and Whisper transcription
    groq_api_key: str = ""
    
    # CORS Settings
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]


settings = Settings()