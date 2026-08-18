from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration from environment variables."""
    
    app_name: str = "House Price Prediction API"
    debug: bool = False
    cors_origins: list = ["http://localhost:5173", "http://localhost:3000"]
    model_path: str = "models/house_price.pkl"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
