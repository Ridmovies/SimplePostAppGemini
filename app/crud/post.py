# app/crud/post.py
"""
Модуль, содержащий функции для выполнения CRUD-операций (Create, Read, Update, Delete)
с моделью Post в базе данных.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate

class CRUDPost:
    """
    Класс, инкапсулирующий CRUD-операции для модели Post.
    """

    async def create_post(self, db: AsyncSession, post_in: PostCreate) -> Post:
        """
        Создает новый пост в базе данных.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
            post_in (PostCreate): Схема Pydantic с данными для создания поста.

        Returns:
            Post: Созданный объект Post из базы данных.
        """
        db_post = Post(**post_in.model_dump()) # model_dump() для Pydantic v2
        # db_post = Post(**post_in.dict()) # для Pydantic v1
        db.add(db_post)
        await db.commit() # Сохраняем изменения в БД
        await db.refresh(db_post) # Обновляем объект из БД, чтобы получить id и timestamps
        return db_post

    async def get_post(self, db: AsyncSession, post_id: int) -> Post | None:
        """
        Получает пост по его идентификатору.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
            post_id (int): Идентификатор поста.

        Returns:
            Post | None: Объект Post, если найден, иначе None.
        """
        result = await db.execute(
            select(Post).filter(Post.id == post_id)
        )
        return result.scalar_one_or_none()

    async def get_posts(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Post]:
        """
        Получает список постов с пагинацией.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
            skip (int): Количество пропускаемых записей.
            limit (int): Максимальное количество возвращаемых записей.

        Returns:
            list[Post]: Список объектов Post.
        """
        result = await db.execute(
            select(Post).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def update_post(self, db: AsyncSession, post_id: int, post_in: PostUpdate) -> Post | None:
        """
        Обновляет существующий пост.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
            post_id (int): Идентификатор поста, который нужно обновить.
            post_in (PostUpdate): Схема Pydantic с обновленными данными поста.

        Returns:
            Post | None: Обновленный объект Post, если найден, иначе None.
        """
        stmt = (
            update(Post)
            .where(Post.id == post_id)
            .values(**post_in.model_dump(exclude_unset=True)) # exclude_unset=True обновляет только переданные поля
            .returning(Post) # Возвращает обновленный объект (для PG 9.5+)
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one_or_none()

    async def delete_post(self, db: AsyncSession, post_id: int) -> Post | None:
        """
        Удаляет пост по его идентификатору.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.
            post_id (int): Идентификатор поста, который нужно удалить.

        Returns:
            Post | None: Удаленный объект Post, если найден, иначе None.
        """
        # Сначала получаем объект, чтобы вернуть его после удаления
        post_to_delete = await self.get_post(db, post_id)
        if not post_to_delete:
            return None

        stmt = delete(Post).where(Post.id == post_id)
        await db.execute(stmt)
        await db.commit()
        return post_to_delete

post_crud = CRUDPost() # Создаем экземпляр класса для удобного импорта