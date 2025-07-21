# tests/conftest.py
from typing import AsyncGenerator

import pytest_asyncio # <-- ДОБАВЬТЕ ЭТОТ ИМПОРТ
from httpx import AsyncClient, ASGITransport


from app.main import app # Убедитесь, что этот импорт теперь работает
from app.core.config import settings
from app.core.database import Base, engine


@pytest_asyncio.fixture(scope="module", autouse=True)
async def prepare_database():
    if settings.MODE != "TEST":
        raise Exception("Тестирование возможно только в режиме 'TEST'")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# Базовая фикстура для создания ЧИСТОГО AsyncClient для каждого теста.
# Этот клиент будет использоваться для неавторизованных запросов.
@pytest_asyncio.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        ac.cookies.clear()
        ac.headers = {}
        yield ac

