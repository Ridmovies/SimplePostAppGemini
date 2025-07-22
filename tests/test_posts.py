# tests/test_posts.py
import pytest
from httpx import AsyncClient

# from app.models.post import Post # Больше не нужно импортировать модель для прямых операций с БД
# from sqlalchemy.ext.asyncio import AsyncSession # Больше не нужно для типизации аргументов теста

# Примечание: порядок выполнения тестов в pytest не гарантируется по умолчанию.
# Если вы полагаетесь на то, что test_create_post создает данные для test_read_posts,
# это может быть хрупким. Для таких сценариев часто используются маркировки
# @pytest.mark.dependency() и @pytest.mark.depends(on=["test_create_post"]).

# Однако, если вы хотите, чтобы каждый тест был независимым,
# КАЖДЫЙ тест должен создавать свои собственные данные через HTTP-эндпоинт
# или у вас должна быть другая фикстура для подготовки данных.

@pytest.mark.asyncio
async def test_create_post(client: AsyncClient):
    """
    Тест создания нового поста через API.
    """
    response = await client.post(
        "/api/v1/posts/",
        json={"title": "Тестовый заголовок", "content": "Это содержимое тестового поста."}
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Тестовый заголовок"
    assert data["content"] == "Это содержимое тестового поста."


@pytest.mark.asyncio
async def test_read_posts(client: AsyncClient):
    """
    Тест чтения списка постов.
    Если предыдущие тесты создали посты, они будут здесь видны.
    Если нужна чистая база, этот подход не подойдет.
    """
    # Предполагается, что база данных может содержать посты из предыдущих тестов.
    # Если вы хотите проверить пустую базу, этот тест нужно запускать первым
    # ИЛИ убедиться, что prepare_database запускается перед каждым тестом (но это "module" scope)
    response = await client.get("/api/v1/posts/")
    assert response.status_code == 200
    data = response.json()
    # Пример: проверяем, что вернулся список, но не делаем предположений о его размере,
    # если тесты зависят друг от друга.
    assert isinstance(data, list)
    # Если вы хотите проверить конкретные посты, вам нужно их создать ВНУТРИ ЭТОГО ТЕСТА
    # или использовать фикстуру для создания.
    # Например, если вы хотите, чтобы этот тест всегда видел 2 поста:
    # await client.post("/api/v1/posts/", json={"title": "Post A", "content": "Content A"})
    # await client.post("/api/v1/posts/", json={"title": "Post B", "content": "Content B"})
    # response = await client.get("/api/v1/posts/")
    # assert len(response.json()) == 2

@pytest.mark.asyncio
async def test_read_single_post(client: AsyncClient):
    """
    Тест чтения одного поста по ID.
    Для этого теста нужно СНАЧАЛА создать пост.
    """
    # Создаем пост, который мы будем читать
    create_response = await client.post(
        "/api/v1/posts/",
        json={"title": "Пост для чтения", "content": "Содержимое для чтения."}
    )
    assert create_response.status_code == 201
    post_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == post_id
    assert data["title"] == "Пост для чтения"

# ---
@pytest.mark.asyncio
async def test_read_single_post_not_found(client: AsyncClient):
    """
    Тест чтения несуществующего поста.
    """
    response = await client.get("/api/v1/posts/999999") # Несуществующий ID
    assert response.status_code == 404
    # assert response.json() == {"detail": "Post not found"}

# ---
@pytest.mark.asyncio
async def test_update_post(client: AsyncClient):
    """
    Тест обновления поста.
    Для этого теста нужно СНАЧАЛА создать пост.
    """
    # Создаем пост для обновления
    create_response = await client.post(
        "/api/v1/posts/",
        json={"title": "Старый заголовок", "content": "Старое содержимое."}
    )
    assert create_response.status_code == 201
    post_id = create_response.json()["id"]

    # Обновляем пост
    update_data = {"title": "Новый заголовок", "content": "Новое содержимое."}
    response = await client.put(f"/api/v1/posts/{post_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == post_id
    assert data["title"] == "Новый заголовок"
    assert data["content"] == "Новое содержимое."

    # Проверяем, что изменения применены
    get_response = await client.get(f"/api/v1/posts/{post_id}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Новый заголовок"

@pytest.mark.asyncio
async def test_update_post_not_found(client: AsyncClient):
    """
    Тест обновления несуществующего поста.
    """
    update_data = {"title": "Что-то", "content": "Что-то еще"}
    response = await client.put("/api/v1/posts/999999", json=update_data)
    assert response.status_code == 404
    # assert response.json() == {"detail": "Post not found"}

# ---
@pytest.mark.asyncio
async def test_delete_post(client: AsyncClient):
    """
    Тест удаления поста.
    Для этого теста нужно СНАЧАЛА создать пост.
    """
    # Создаем пост для удаления
    create_response = await client.post(
        "/api/v1/posts/",
        json={"title": "Пост для удаления", "content": "Содержимое для удаления."}
    )
    assert create_response.status_code == 201
    post_id = create_response.json()["id"]

    response = await client.delete(f"/api/v1/posts/{post_id}")
    assert response.status_code == 200 # Обычно 204 No Content при успешном удалении
    # assert response.content == b"" # Тело ответа должно быть пустым

    # Проверяем, что пост действительно удален
    get_response = await client.get(f"/api/v1/posts/{post_id}")
    assert get_response.status_code == 404 # Теперь пост не найден

@pytest.mark.asyncio
async def test_delete_post_not_found(client: AsyncClient):
    """
    Тест удаления несуществующего поста.
    """
    response = await client.delete("/api/v1/posts/999999")
    assert response.status_code == 404
    # assert response.json() == {"detail": "Post not found"}