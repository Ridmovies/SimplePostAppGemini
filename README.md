# SimplePostApp

[![Build Status](https://img.shields.io/badge/Status-In%20Development-blue)](link_to_ci_cd_status)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## Описание проекта

**SimplePostApp** — это минималистичное веб-приложение, разработанное с использованием **FastAPI**, **PostgreSQL** (через SQLAlchemy ORM), и **Docker Compose**. Приложение предназначено для создания, чтения, обновления и удаления (CRUD) постов. Оно спроектировано с акцентом на **масштабируемость, безопасность** и **лучшие практики** разработки, что делает его отличной отправной точкой для более сложных проектов. Включает в себя интеграцию с **Alembic** для миграций базы данных, **Pytest** для тестирования и простой фронтенд на **Jinja2** для демонстрации.

## Используемые технологии

* **Бэкенд:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.11+)
* **База данных:** [PostgreSQL](https://www.postgresql.org/)
* **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
* **Миграции БД:** [Alembic](https://alembic.sqlalchemy.org/en/latest/)
* **Валидация данных:** [Pydantic](https://pydantic-docs.helpmanual.io/)
* **ASGI-сервер:** [Uvicorn](https://www.uvicorn.org/)
* **Контейнеризация:** [Docker](https://www.docker.com/), [Docker Compose](https://docs.docker.com/compose/)
* **Тестирование:** [Pytest](https://docs.pytest.org/)
* **Шаблонизатор:** [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/)
* **Управление зависимостями:** [pip](https://pip.pypa.io/en/stable/) (можно заменить на Poetry)

## Структура проекта

```code
├── .env.example              # Пример файла переменных окружения
├── .gitignore                # Файл для Git: какие файлы игнорировать
├── alembic.ini               # Конфигурация Alembic для миграций БД
├── docker-compose.yml        # Конфигурация Docker Compose
├── Dockerfile                # Dockerfile для сборки образа приложения
├── pyproject.toml            # Конфигурация Poetry (или requirements.txt для pip)
├── README.md                 # Описание проекта
├── alembic/                  # Директория для миграций Alembic
│   ├── versions/             # Сгенерированные файлы миграций
│   └── env.py                # Скрипт окружения Alembic
├── app/                      # Основная директория приложения
│   ├── core/                 # Основные компоненты и настройки
│   │   ├── config.py         # Настройки приложения (переменные окружения)
│   │   └── database.py       # Конфигурация базы данных и сессии
│   ├── crud/                 # Create, Read, Update, Delete операции с БД
│   │   └── post.py           # CRUD-операции для модели Post
│   ├── models/               # Модели SQLAlchemy
│   │   └── post.py           # Определение модели Post
│   ├── schemas/              # Схемы Pydantic для валидации и сериализации
│   │   └── post.py           # Схемы для Post (создание, чтение)
│   ├── api/                  # API-эндпоинты
│   │   ├── endpoints/        # Различные группы эндпоинтов
│   │   │   └── posts.py      # Эндпоинты для постов
│   │   └── init.py       # Регистрация API маршрутов
│   ├── templates/            # HTML-шаблоны Jinja2
│   │   └── index.html        # Главный шаблон
│   └── main.py               # Главный файл приложения FastAPI
├── tests/                    # Директория для тестов
│   ├── conftest.py           # Фикстуры для Pytest
│   └── test_posts.py         # Тесты для API постов
└── venv/                     # Виртуальное окружение (игнорируется Git)
```

## Установка и запуск (Локально без Docker)

1.  **Клонируйте репозиторий:**
    ```bash
    git clone [https://github.com/your-username/SimplePostApp.git](https://github.com/your-username/SimplePostApp.git)
    cd SimplePostApp
    ```

2.  **Создайте и активируйте виртуальное окружение:**
    ```bash
    python -m venv venv
    source venv/bin/activate # Для Linux/macOS
    # venv\Scripts\activate   # Для Windows
    ```

3.  **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Настройте переменные окружения:**
    Создайте файл `.env` в корневой директории проекта, скопировав содержимое из `.env.example` и заполнив актуальные данные для вашей локальной базы данных PostgreSQL.
    ```ini
    # .env
    DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/simplepostapp_db"
    SECRET_KEY="your-local-dev-secret-key"
    ```
    Убедитесь, что у вас есть локальный PostgreSQL сервер, и создайте базу данных `simplepostapp_db` с соответствующими учетными данными.

5.  **Запустите Alembic для создания таблиц (первоначальная миграция):**
    Установите Alembic, если еще не установлен: `pip install alembic`.
    Инициализируйте Alembic (только один раз, если еще не было): `alembic init alembic`
    **Важно:** Для этого проекта Alembic уже настроен. Вам нужно только убедиться, что он работает.
    Генерировать миграции и применять их:
    ```bash
    # Сгенерировать первую миграцию (если еще нет)
    # alembic revision --autogenerate -m "Initial migration"
    # Применить миграции к БД
    alembic upgrade head
    ```
    *Примечание: в `app/main.py` есть временный `Base.metadata.create_all` для быстрой разработки. Для продакшена используйте Alembic.*

6.  **Запустите приложение:**
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    Приложение будет доступно по адресу `http://127.0.0.1:8000`.

## Запуск с Docker Compose

Это предпочтительный способ запуска для разработки и демонстрации.

1.  **Убедитесь, что установлен Docker Desktop.**

2.  **Создайте `.env` файл:**
    В корневой директории проекта создайте файл `.env` (не `.env.example`) с необходимыми переменными окружения. Эти переменные будут использоваться сервисами Docker Compose.
    ```ini
    # .env
    DATABASE_URL="postgresql+asyncpg://user:password@db:5432/simplepostapp_db"
    POSTGRES_USER=user
    POSTGRES_PASSWORD=password
    POSTGRES_DB=simplepostapp_db
    SECRET_KEY="your-strong-random-secret-key-for-docker"
    ```
    Обратите внимание, что `DATABASE_URL` теперь ссылается на сервис `db` внутри Docker сети.

3.  **Запустите сервисы Docker Compose:**
    ```bash
    docker compose up --build -d
    ```
    Эта команда соберет Docker-образ для приложения (если еще не собран или есть изменения) и запустит контейнеры FastAPI и PostgreSQL в фоновом режиме.

4.  **Проверьте статус контейнеров:**
    ```bash
    docker compose ps
    ```

5.  **Доступ к приложению:**
    Приложение будет доступно по адресу `http://localhost:8000`.
    * Документация API (Swagger UI): `http://localhost:8000/docs`
    * Документация API (ReDoc): `http://localhost:8000/redoc`

6.  **Остановка контейнеров:**
    ```bash
    docker compose down
    ```

## API Эндпоинты

Все API эндпоинты доступны по префиксу `/api/v1`. Полная документация доступна через Swagger UI (`/docs`).

* **`POST /api/v1/posts/`**: Создать новый пост.
* **`GET /api/v1/posts/`**: Получить список всех постов.
* **`GET /api/v1/posts/{post_id}`**: Получить пост по ID.
* **`PUT /api/v1/posts/{post_id}`**: Обновить существующий пост.
* **`DELETE /api/v1/posts/{post_id}`**: Удалить пост по ID.

## Тестирование

Проект включает набор тестов с использованием Pytest.

1.  **Подготовьте тестовую базу данных:**
    Создайте отдельную базу данных для тестов в PostgreSQL (например, `test_simplepostapp_db`) и предоставьте к ней доступ.
    ```sql
    CREATE DATABASE test_simplepostapp_db;
    CREATE USER user WITH PASSWORD 'password'; -- Используйте те же user/password, что и в .env
    GRANT ALL PRIVILEGES ON DATABASE test_simplepostapp_db TO user;
    ```
    Убедитесь, что `DATABASE_URL` в `tests/conftest.py` указывает на эту тестовую базу.

2.  **Запустите тесты:**
    ```bash
    pytest
    ```

## Миграции базы данных (Alembic)

Для управления изменениями в схеме базы данных используется Alembic.

1.  **Инициализация Alembic (если требуется):**
    ```bash
    alembic init alembic
    ```
    *(Уже сделано в проекте)*

2.  **Генерация миграции:**
    После изменения моделей SQLAlchemy (в `app/models/`), вы можете сгенерировать новую миграцию:
    ```bash
    alembic revision --autogenerate -m "Added new column to Post"
    ```

3.  **Применение миграций:**
    ```bash
    alembic upgrade head
    ```

4.  **Откат миграций (на предыдущую версию):**
    ```bash
    alembic downgrade -1
    ```

## Безопасность и лучшие практики

* **Валидация данных:** Использование Pydantic для строгой валидации входных и выходных данных, что предотвращает многие распространенные уязвимости (например, SQL-инъекции через некорректные данные).
* **Разделение ответственности:** Код разделен на логические слои (API, CRUD, модели, схемы), что улучшает читаемость, поддерживаемость и масштабируемость.
* **Переменные окружения:** Конфигурация приложения через `.env` файлы и переменные окружения обеспечивает безопасное хранение чувствительных данных.
* **Асинхронность:** Использование `async/await` и асинхронных драйверов БД (`asyncpg`) для повышения производительности и лучшей обработки конкурентных запросов.
* **Миграции БД:** Alembic обеспечивает контролируемый и безопасный процесс изменения схемы базы данных.
* **Тестирование:** Pytest с фикстурами для изоляции тестов и использования отдельной БД гарантирует стабильность и корректность работы приложения.
* **Докер и Docker Compose:** Изоляция среды выполнения, воспроизводимость и легкое развертывание.

## Дальнейшее развитие

* **Аутентификация и авторизация:** Добавление JWT-токенов или OAuth2 для защиты API.
* **Обработка ошибок:** Более детальная и унифицированная обработка ошибок.
* **Логирование:** Интеграция с библиотекой логирования (например, `logging` из стандартной библиотеки Python).
* **Кэширование:** Использование Redis для кэширования часто запрашиваемых данных.
* **Очереди задач:** Интеграция с Celery или другим брокером сообщений для выполнения долгих задач в фоне.
* **Развертывание:** Добавление конфигураций для облачных провайдеров (AWS, Google Cloud, Azure) или Kubernetes.

## Итого:
- нет .gitignore
- нет .dockerignore
- полностью не работает пайтест


