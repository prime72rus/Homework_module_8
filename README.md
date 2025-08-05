# Backend-часть SPA-приложения "Платформа для обучения"
### Контекст
В данном проекте реализована backend-часть приложения для обучения (API), содержащее:
- регистрация и аутентификация пользователей;
- создание, обновление, удаление курса;
- создание, обновление, удаление уроков;
- возможность подписки на обновление курса;
- оплата курса или урока отдельно.

## Содержание
- [Технологии](#технологии)
- [Начало работы](#начало-работы)
- [Команда проекта](#команда-проекта)

## Технологии
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Celery](https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html)
- [Celery-beat](https://django-celery-beat.readthedocs.io/en/latest/)
- [Poetry](https://python-poetry.org/)
- [Redis](https://pypi.org/project/redis/)
- [PostgreSQL](https://www.postgresql.org/)

## Начало работы
Клонируйте репозиторий по ссылке https://github.com/prime72rus/Homework_module_8.git
```python
git clone https://github.com/prime72rus/Homework_module_8.git
```
Установите Poetry.
Создайте виртуальное окружение:
```python
poetry init
```
Установите зависимости:
```python
poetry install
```
По шаблону `.env.sample` создайте и заполните в корневой папке проекта файл `.env`.  
Установите Docker и Docker Compose, если они ещё не установлены.
В терминале, перейдите в директорию проекта.
Запустите команду:
```python
docker-compose up --build
```
### Документация по использованию API приложения
При запущенном приложении:  
http://localhost:8000/swagger/  
http://localhost:8000/redoc/

### Проверка работоспособности

- **Backend**: Откройте браузер и перейдите по адресу `http://localhost:8000`.
- **PostgreSQL**: Подключитесь к базе данных через pgAdmin или другой клиент.
- **Redis**: Используйте `redis-cli` для проверки подключения.
В терминале выполните команду:
```python
docker exec -it homework_module_8-redis-1 redis-cli
```
Проверка соединения:
```python
127.0.0.1:6379> PING
```

- **Celery** и **Celery Beat**: Проверьте логи в терминале, чтобы убедиться, что задачи выполняются без ошибок.`
```python
docker-compose logs celery_worker
```
```python
docker-compose logs celery_beat
```

## Команда проекта

- Dmitrii Grechko tg:@prime72rus
