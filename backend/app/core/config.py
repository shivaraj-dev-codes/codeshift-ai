"""
Application configuration and environment settings
"""

from typing import List
from functools import lru_cache

from pydantic_settings import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Core
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    API_VERSION: str = "v1"
    API_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://codeshift:codeshift_dev_password@localhost:5432/codeshift_ai",
        env="DATABASE_URL",
    )
    DATABASE_POOL_SIZE: int = Field(default=20, env="DATABASE_POOL_SIZE")
    DATABASE_MAX_OVERFLOW: int = Field(default=10, env="DATABASE_MAX_OVERFLOW")

    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    REDIS_CACHE_TTL: int = Field(default=3600, env="REDIS_CACHE_TTL")  # 1 hour

    # Qdrant Vector DB
    QDRANT_URL: str = Field(default="http://localhost:6333", env="QDRANT_URL")
    QDRANT_API_KEY: str = Field(default="qdrant_api_key_dev", env="QDRANT_API_KEY")
    QDRANT_COLLECTION_NAME: str = "code_embeddings"
    VECTOR_DIMENSION: int = 1536  # OpenAI embedding dimension

    # Security
    JWT_SECRET: str = Field(default="your-super-secret-jwt-key-change-in-prod", env="JWT_SECRET")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    REFRESH_TOKEN_EXPIRATION_DAYS: int = 30

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
    ]
    ALLOWED_HOSTS: List[str] = ["*"]  # Update in production

    # OAuth
    GITHUB_CLIENT_ID: str = Field(default="", env="GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET: str = Field(default="", env="GITHUB_CLIENT_SECRET")
    GITHUB_REDIRECT_URI: str = Field(default="http://localhost:8000/api/v1/auth/github/callback", env="GITHUB_REDIRECT_URI")

    # LLM & AI
    OPENAI_API_KEY: str = Field(default="", env="OPENAI_API_KEY")
    GEMINI_API_KEY: str = Field(default="", env="GEMINI_API_KEY")
    LLM_MODEL: str = Field(default="gpt-4", env="LLM_MODEL")
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 2000

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_API_REQUESTS: int = 1000  # per hour
    RATE_LIMIT_UPLOAD: int = 10  # per day
    RATE_LIMIT_CHAT: int = 100  # per hour
    RATE_LIMIT_ANALYSIS: int = 50  # per day

    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 500
    UPLOAD_TEMP_DIR: str = "/tmp/codeshift_uploads"
    ALLOWED_EXTENSIONS: List[str] = ["zip"]

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = "json"  # json or text

    # Analytics
    ANALYTICS_ENABLED: bool = True
    TELEMETRY_ENABLED: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
