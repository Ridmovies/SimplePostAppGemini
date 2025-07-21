# tests/test_posts.py
"""
Тесты для API-эндпоинтов, связанных с постами.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.post import Post # Импортируем модель для прямого взаимодействия с БД в тестах


@pytest.mark.asyncio
async def test_create_post(client):
    """
    Тест создания нового поста.
    """
    response = await client.post(
        "/api/v1/posts/",
        json={"title": "Тестовый заголовок", "content": "Это содержимое тестового поста."}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Тестовый заголовок"
    assert data["content"] == "Это содержимое тестового поста."
    assert "id" in data
    assert "created_at" in data

@pytest.mark.asyncio
async def test_read_posts(client: AsyncClient):
    """
    Тест чтения списка постов.
    """


    response = await client.get("/api/v1/posts/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1 # Могут быть посты из других тестов (если rollback не сработал корректно)


@pytest.mark.asyncio
async def test_read_single_post(client: AsyncClient, db_session: AsyncSession):
    """
    Тест чтения одного поста по ID.
    """
    test_post = Post(title="Одиночный пост", content="Это содержимое одиночного поста.")
    db_session.add(test_post)
    await db_session.commit()
    await db_session.refresh(test_post)

    response = await client.get(f"/api/v1/posts/{test_post.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_post.id
    assert data["title"] == "Одиночный пост"

@pytest.mark.asyncio
async def test_read_single_post_not_found(client: AsyncClient):
    """
    Тест чтения несуществующего поста.
    """
    response = await client.get("/api/v1/posts/99999") # Несуществующий ID
    assert response.status_code == 404
    assert response.json()["detail"] == "Пост не найден"

@pytest.mark.asyncio
async def test_update_post(client: AsyncClient, db_session: AsyncSession):
    """
    Тест обновления поста.
    """
    test_post = Post(title="Старый заголовок", content="Старое содержимое.")
    db_session.add(test_post)
    await db_session.commit()
    await db_session.refresh(test_post)

    update_data = {"title": "Новый заголовок", "content": "Новое содержимое."}
    response = await client.put(f"/api/v1/posts/{test_post.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_post.id
    assert data["title"] == "Новый заголовок"
    assert data["content"] == "Новое содержимое."
    assert data["updated_at"] is not None

@pytest.mark.asyncio
async def test_update_post_not_found(client: AsyncClient):
    """
    Тест обновления несуществующего поста.
    """
    update_data = {"title": "Новый заголовок"}
    response = await client.put("/api/v1/posts/99999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Пост не найден"

@pytest.mark.asyncio
async def test_delete_post(client: AsyncClient, db_session: AsyncSession):
    """
    Тест удаления поста.
    """
    test_post = Post(title="Пост для удаления", content="Это пост, который будет удален.")
    db_session.add(test_post)
    await db_session.commit()
    await db_session.refresh(test_post)

    response = await client.delete(f"/api/v1/posts/{test_post.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_post.id
    assert data["title"] == "Пост для удаления"

    # Проверяем, что пост действительно удален
    get_response = await client.get(f"/api/v1/posts/{test_post.id}")
    assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_delete_post_not_found(client: AsyncClient):
    """
    Тест удаления несуществующего поста.
    """
    response = await client.delete("/api/v1/posts/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Пост не найден"