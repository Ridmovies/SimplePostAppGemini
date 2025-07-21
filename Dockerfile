# Dockerfile
# Используем официальный образ Python как базовый
FROM python:3.11-slim-bookworm

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED 1 \
    PIP_NO_CACHE_DIR 1

# Устанавливаем зависимости для работы с PostgreSQL (libpq-dev)
# и для сборки некоторых Python пакетов (build-essential)
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        postgresql-client \
        libpq-dev \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей requirements.txt
COPY requirements.txt /app/

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код приложения в рабочую директорию
COPY . /app

# Открываем порт, на котором будет слушать FastAPI
EXPOSE 8000

# Команда для запуска приложения с Uvicorn
# --host 0.0.0.0 позволяет приложению слушать на всех сетевых интерфейсах
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]