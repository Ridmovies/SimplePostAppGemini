# app/api/__init__.py
"""
Инициализация API-маршрутов для различных групп эндпоинтов.
"""

from fastapi import APIRouter

from app.api.endpoints import posts


api_router = APIRouter()

# Включаем маршруты для постов под префиксом /posts
api_router.include_router(posts.router, prefix="/posts", tags=["Посты"])