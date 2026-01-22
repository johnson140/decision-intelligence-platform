"""
Application configuration settings
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS Settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # Data Settings
    DATA_DIR: str = "data"
    UPLOAD_DIR: str = "data/uploads"
    
    # Business Logic Settings
    SLOW_MOVING_THRESHOLD_DAYS: int = 90  # Days without sales to be considered slow-moving
    LOW_STOCK_THRESHOLD_PERCENT: float = 0.2  # 20% of average stock level
    REORDER_LEAD_TIME_DAYS: int = 7  # Average lead time for reorders


settings = Settings()
