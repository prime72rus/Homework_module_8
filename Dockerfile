FROM python:3.13
# Устанавливаем рабочую директорию
WORKDIR /app
# Устанавливаем системные зависимости
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    gcc \
    libpq-dev \
    python3-dev \
    postgresql-server-dev-15 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Устанавливаем Poetry
RUN pip install poetry==1.8.4
RUN poetry config virtualenvs.create false
# Добавляем Poetry в PATH
ENV PATH="/root/.local/bin:${PATH}"
# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./
# Устанавливаем Python-зависимости
RUN poetry install --no-interaction --no-ansi --only main
# Копируем остальные файлы проекта
COPY . .
# Создаем директорию для медиафайлов
RUN mkdir -p /app/{static,media}
# Открываем порт
EXPOSE 8000
# Команда запуска
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
