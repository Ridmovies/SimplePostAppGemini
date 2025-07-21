# app/core/config.py
"""
Модуль для управления конфигурацией приложения с использованием переменных окружения.
"""
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Класс для загрузки настроек приложения из переменных окружения.

    Использует Pydantic BaseSettings для автоматической валидации и загрузки.
    Переменные окружения будут прочитаны из файла .env.
    """
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')  # Pydantic v2


    # Для Pydantic v1 (если вдруг используется более старая версия)
    # class Config:
    #     env_file = ".env"
    #     extra = 'ignore' # Игнорировать дополнительные переменные окружения

    # Указываем .env файл для Pydantic-settings
    # model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

    MODE: Literal["DEV", "TEST", "PROD"] = "DEV"

    # Настройки базы данных
    DATABASE_URL: str
    # Пример: postgresql+asyncpg://user:password@host:port/dbname

    TEST_DB_URL: str

    # Настройки приложения
    PROJECT_NAME: str = "SimplePostApp"
    API_V1_STR: str = "/api/v1"

    # Секретный ключ для будущих функций (например, JWT) - обязательно генерируйте сложный!
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

settings = Settings()