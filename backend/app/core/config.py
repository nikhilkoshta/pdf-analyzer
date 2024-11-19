from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from pathlib import Path

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "PDF QA System"
    
    # Database
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # Security
    SECRET_KEY: str = "nikhil-pdf-secret"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # OpenAI
    OPENAI_API_KEY: str
    
    # File Storage
    UPLOAD_DIR: str = "uploads"
    VECTOR_STORE_DIR: str = "vector_stores"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"

    def create_upload_dir(self):
        """Create upload directory if it doesn't exist"""
        Path(self.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.VECTOR_STORE_DIR).mkdir(parents=True, exist_ok=True)

@lru_cache()
def get_settings():
    settings = Settings()
    settings.create_upload_dir()
    return settings

settings = get_settings()