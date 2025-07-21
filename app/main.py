# app/main.py
"""
Главный файл FastAPI-приложения SimplePostApp.
Настраивает основные маршруты, шаблоны и обработчики событий.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api import api_router
from app.core.database import engine, Base # Импортируем engine и Base для создания таблиц при запуске (только для dev)
import os

# Инициализируем FastAPI приложение
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs", # URL для Swagger UI
    redoc_url="/redoc" # URL для ReDoc
)

# Монтируем статические файлы (если есть)
# app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Настраиваем Jinja2 шаблоны
templates = Jinja2Templates(directory="app/templates")

# Включаем API-мартеры
app.include_router(api_router, prefix=settings.API_V1_STR)

# @app.on_event("startup")
# async def startup_event():
#     """
#     Обработчик события запуска приложения.
#     Создает таблицы базы данных при старте (только для разработки!).
#     Для продакшена используйте Alembic миграции.
#     """
#     print("Запуск приложения...")
#     # Внимание: В продакшене не используйте Base.metadata.create_all,
#     # а используйте Alembic для управления миграциями БД.
#     # Здесь это сделано для простоты демонстрации и быстрой разработки.
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     print("Таблицы БД проверены/созданы.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Таблицы БД проверены/созданы.")
    yield

@app.get("/", response_class=HTMLResponse)
async def read_root_frontend(request: Request):
    """
    Корневой эндпоинт для отображения главной страницы фронтенда.
    """
    return templates.TemplateResponse("index.html", {"request": request, "project_name": settings.PROJECT_NAME})