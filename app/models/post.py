# app/models/post.py
"""
Модуль, определяющий модель данных Post для SQLAlchemy ORM.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Post(Base):
    """
    Модель Post, представляющая таблицу 'posts' в базе данных.
    """
    __tablename__ = "posts" # Имя таблицы в БД

    id = Column(Integer, primary_key=True, index=True) # Первичный ключ, индексируем для быстрого поиска
    title = Column(String(256), index=True, nullable=False) # Заголовок поста, не может быть null
    content = Column(Text, nullable=False) # Содержимое поста, может быть длинным текстом
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # Время создания, автоматически заполняется при создании
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) # Время последнего обновления, автоматически обновляется

    def __repr__(self):
        """
        Представление объекта Post для отладки.
        """
        return f"<Post(id={self.id}, title='{self.title}')>"