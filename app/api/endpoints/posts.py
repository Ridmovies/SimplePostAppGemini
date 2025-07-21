# app/api/endpoints/posts.py
"""
Модуль, содержащий API-эндпоинты для управления постами.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.post import PostCreate, PostUpdate, PostInDB
from app.crud.post import post_crud
from app.core.database import get_db

router = APIRouter()

@router.post("/", response_model=PostInDB, status_code=status.HTTP_201_CREATED)
async def create_new_post(
    post_in: PostCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Создает новый пост.

    Args:
        post_in (PostCreate): Данные для нового поста.
        db (AsyncSession): Сессия базы данных.

    Returns:
        PostInDB: Созданный пост.
    """
    return await post_crud.create_post(db=db, post_in=post_in)

@router.get("/", response_model=List[PostInDB])
async def read_posts(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Получает список всех постов.

    Args:
        skip (int): Количество пропускаемых постов.
        limit (int): Максимальное количество возвращаемых постов.
        db (AsyncSession): Сессия базы данных.

    Returns:
        List[PostInDB]: Список постов.
    """
    posts = await post_crud.get_posts(db=db, skip=skip, limit=limit)
    return posts

@router.get("/{post_id}", response_model=PostInDB)
async def read_post_by_id(
    post_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Получает пост по его ID.

    Args:
        post_id (int): ID поста.
        db (AsyncSession): Сессия базы данных.

    Returns:
        PostInDB: Найденный пост.

    Raises:
        HTTPException: Если пост не найден.
    """
    post = await post_crud.get_post(db=db, post_id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден"
        )
    return post

@router.put("/{post_id}", response_model=PostInDB)
async def update_existing_post(
    post_id: int,
    post_in: PostUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Обновляет существующий пост.

    Args:
        post_id (int): ID поста для обновления.
        post_in (PostUpdate): Данные для обновления поста.
        db (AsyncSession): Сессия базы данных.

    Returns:
        PostInDB: Обновленный пост.

    Raises:
        HTTPException: Если пост не найден.
    """
    updated_post = await post_crud.update_post(db=db, post_id=post_id, post_in=post_in)
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден"
        )
    return updated_post

@router.delete("/{post_id}", response_model=PostInDB)
async def delete_existing_post(
    post_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Удаляет пост по его ID.

    Args:
        post_id (int): ID поста для удаления.
        db (AsyncSession): Сессия базы данных.

    Returns:
        PostInDB: Удаленный пост.

    Raises:
        HTTPException: Если пост не найден.
    """
    deleted_post = await post_crud.delete_post(db=db, post_id=post_id)
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден"
        )
    return deleted_post