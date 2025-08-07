FROM python:3.13

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    gcc \
    libpq-dev \
    python3-dev \
    postgresql-server-dev-15 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.8.4
RUN poetry config virtualenvs.create false

ENV PATH="/root/.local/bin:${PATH}"

COPY pyproject.toml ./

RUN poetry install --no-interaction --no-ansi --only main

COPY . .

RUN mkdir -p /app/staticfiles

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]
