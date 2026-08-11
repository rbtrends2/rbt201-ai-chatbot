"""Application configuration loaded from environment variables."""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings with safe demo defaults."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "RBT201 AI Chatbot"
    ai_provider: Literal["demo", "openai_compatible"] = "demo"
    openai_api_key: str | None = Field(default=None, repr=False)
    openai_base_url: str = "https://api.openai.com/v1/chat/completions"
    openai_model: str = "gpt-4o-mini"
    max_context_chars: int = Field(default=6000, ge=500, le=20000)
    request_timeout_seconds: float = Field(default=20.0, gt=0, le=120)
    cors_origins: str = "http://127.0.0.1:8000,http://localhost:8000"

    @property
    def cors_origin_list(self) -> list[str]:
        """Return configured origins without blank entries."""
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the process-wide validated settings instance."""
    return Settings()
