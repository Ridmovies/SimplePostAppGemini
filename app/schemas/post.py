# app/schemas/post.py
"""
Модуль, определяющий Pydantic-схемы для модели Post.
Используются для валидации входных данных API и форматирования выходных данных.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    """
    Базовая схема для Post, содержащая общие поля.
    """
    title: str = Field(..., min_length=1, max_length=256)
    content: str = Field(..., min_length=10)

class PostCreate(PostBase):
    """
    Схема для создания нового поста. Наследует PostBase.
    Дополнительных полей для создания не требуется, так как timestamp'ы генерируются БД.
    """
    pass

class PostUpdate(PostBase):
    """
    Схема для обновления существующего поста.
    Все поля опциональны, так как можно обновить только часть полей.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=256)
    content: Optional[str] = Field(None, min_length=10)


class PostInDB(PostBase):
    """
    Схема для чтения поста из базы данных, включающая поля,
    которые генерируются или управляются базой данных.
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None # updated_at может быть None, если пост никогда не обновлялся

    # class Config:
    #     """
    #     Конфигурация Pydantic-модели.
    #     from_attributes = True (бывший orm_mode = True) позволяет Pydantic читать данные
    #     напрямую из ORM-моделей SQLAlchemy.
    #     """
    #     from_attributes = True # Для Pydantic v2
    #     # orm_mode = True # Для Pydantic v1