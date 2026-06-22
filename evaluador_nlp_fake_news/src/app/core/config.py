from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "Evaluador Fake News BETO vs mBERT"
    DATABASE_URL: str = "sqlite:///./evaluation_results.db"
    MODEL_CACHE_DIR: str = "./model_cache"
    LOG_LEVEL: str = "INFO"
    
    # Additional configuration from .env
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 4
    DATABASE_PATH: str = "evaluation_results.db"
    MAX_TEXT_LENGTH: int = 512
    BATCH_SIZE: int = 32
    LOG_FILE: str = "app.log"
    CORS_ORIGINS: str = "*"
    SECRET_KEY: str = "your-secret-key-here"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
