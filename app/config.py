"""Application configuration using pydantic-settings."""
import logging
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME:        str = "Address Book API"
    APP_VERSION:     str = "1.0.0"
    APP_DESCRIPTION: str = "Create, update, delete and search addresses by proximity."
    DEBUG:           bool = False

    # Database
    DATABASE_URL: str = "sqlite:///./address_book.db"

    # Pagination
    DEFAULT_SKIP:  int = 0
    DEFAULT_LIMIT: int = 100

    # Earth radius for Haversine
    EARTH_RADIUS_KM: float = 6371.0

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }


settings = Settings()