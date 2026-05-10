from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "WMS AI"
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    AI_API_KEY: str
    AI_MODEL: str = "gpt-4o-mini"
    CORS_ORIGINS: list[str] = ["*"]
    
    class model_config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()