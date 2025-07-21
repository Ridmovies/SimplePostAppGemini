# app/core/database.py
"""
Модуль для настройки соединения с базой данных PostgreSQL с помощью SQLAlchemy.
Определяет асинхронный движок, фабрику сессий и базовый класс для декларативных моделей.
"""
from typing import AsyncGenerator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import settings
import asyncio

# Создаем асинхронный движок SQLAlchemy
# echo=True для логирования SQL-запросов (отключить в продакшене)


# Определяем параметры подключения к БД в зависимости от режима работы (тестовый/обычный)
if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DB_URL  # URL тестовой БД
    DATABASE_PARAMS = {"poolclass": NullPool}  # Отключаем пул соединений для тестов
else:
    DATABASE_URL = settings.DATABASE_URL  # URL основной БД
    DATABASE_PARAMS = {}  # Используем стандартный пул соединений


engine = create_async_engine(DATABASE_URL, echo=False, **DATABASE_PARAMS)

# Создаем асинхронную фабрику сессий
# expire_on_commit=False предотвращает истечение срока действия объектов после commit,
# что полезно для работы с объектами вне сессии.
# AsyncSessionLocal = async_sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine,
#     class_=AsyncSession,
#     expire_on_commit=False # Очень важно для асинхронного SQLAlchemy
# )

async_session = async_sessionmaker(engine, expire_on_commit=False)

# Асинхронный генератор для получения сессии БД
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:  # Создаем новую сессию
        yield session  # Возвращаем сессию через yield (паттерн dependency injection)


Base = declarative_base()

# async def get_db():
#     """
#     Генератор зависимостей для FastAPI, предоставляющий асинхронную сессию БД.
#     Сессия автоматически закрывается после завершения запроса.
#     """
#     db: AsyncSession = AsyncSessionLocal()
#     try:
#         yield db
#     finally:
#         await db.close()

# Пример использования (не обязательно для FastAPI, но полезно для отладки)
async def test_db_connection():
    """
    Функция для проверки соединения с базой данных.
    """
    try:
        async with engine.connect() as connection:
            await connection.execute("SELECT 1")
            print("Успешное подключение к базе данных!")
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")

if __name__ == "__main__":
    # Запускаем проверку соединения при прямом запуске файла
    asyncio.run(test_db_connection())