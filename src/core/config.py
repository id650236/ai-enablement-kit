"""Zentrale Konfiguration für das AI Enablement Kit.

Lädt Einstellungen aus Umgebungsvariablen (.env) via pydantic-settings.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Anwendungs-Einstellungen.

    Werte werden aus .env oder Umgebungsvariablen geladen.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        protected_namespaces=(),
    )

    # Anthropic / Claude
    anthropic_api_key: str = "sk-ant-placeholder"
    model_name: str = "claude-sonnet-4-6"

    # Datenbank
    database_url: str = "sqlite:///./data/knowledge.db"

    # Logging
    log_level: str = "INFO"

    # App
    app_name: str = "AI Enablement Kit"
    app_version: str = "0.1.0"


@lru_cache
def get_settings() -> Settings:
    """Gibt die gecachte Settings-Instanz zurück."""
    return Settings()