import os
from pydantic import BaseModel
from typing import List

class Settings(BaseModel):
    APP_NAME: str = "IncuBrix AEO, SEO & GEO Visibility Engine"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    TARGET_WEBSITE: str = "https://incubrix.com"
    PORT: int = int(os.getenv("PORT", "8001"))
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./incubrix.db")
    
    # Redis / Celery
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Providers
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    PERPLEXITY_API_KEY: str = os.getenv("PERPLEXITY_API_KEY", "")
    SEARCH_API_KEY: str = os.getenv("SEARCH_API_KEY", "")
    PAGESPEED_API_KEY: str = os.getenv("PAGESPEED_API_KEY", "")
    APP_SECRET: str = os.getenv("APP_SECRET", "incubrix-super-secret-key-change-in-production")
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8001",
        "http://127.0.0.1:8001",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]

settings = Settings()
