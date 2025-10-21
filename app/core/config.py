from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_DB_NAME: str
    POSTGRES_USER_NAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB_URL: str
    API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    """Возвращает экземпрял класса настроек"""
    return Settings()


def reload_settings() -> Settings:
    """Очищает кэш и возвращает обновлённые настройки."""
    get_settings.cache_clear()
    return get_settings()


settings = get_settings()
