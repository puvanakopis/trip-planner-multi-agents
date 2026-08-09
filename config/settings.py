import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "CeylonTrip AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # LLM Settings
    GROQ_API_KEY: str = ""
    DEFAULT_MODEL: str = "llama-3.3-70b-versatile"
    LLM_TEMPERATURE: float = 0.0

    # API Keys & Endpoints (Optional external providers)
    HOTEL_API_KEY: str = ""
    RAPIDAPI_KEY: str = ""
    MAPS_API_KEY: str = ""
    
    # Rate Limiting & Timeouts
    HTTP_TIMEOUT_SECONDS: int = 15
    MAX_RETRIES: int = 3

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
