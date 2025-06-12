from pydantic import BaseModel
from typing import Optional
from functools import lru_cache

class Settings(BaseModel):
    """Application settings."""
    APP_NAME: str = "Fake User Data API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "An API for generating fake user data"
    CACHE_TTL: int = 3600  # Cache time to live in seconds
    DEFAULT_LOCALE: str = "en_US"
    MAX_USERS_PER_REQUEST: int = 100
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings."""
    return Settings() 