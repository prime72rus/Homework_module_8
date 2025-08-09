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
- [Деплой на удаленный сервер](#deploy-на-удаленный-сервер-)
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
Установите Docker Desktop (Docker и Docker Compose), если они ещё не установлены.
В терминале, перейдите в директорию проекта.
Запустите команду:
```python
docker-compose up
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

## Deploy на удаленный сервер  

Скопируйте проект в репозиторий на GitHub.
По шаблону .env.sample создайте переменные в Repository secrets GitHub

### Виртуальная машина
Перед развертыванием приложения, настройте виртуальную машину с ОС Linux Ubuntu 24.04 LTS.  
Для этого воспользуйтесь специальными средствами, например Yandex Cloud.  
На запущенном сервере сгенерируйте SSH-ключ для безопасного удаленного подключения к серверу.
```python
ssh-keygen -t ed25519 -C "ваш_email@example.com"
```

### Обновление системы
Откройте терминал и выполните команду для обновления списка пакетов:
```python
sudo apt update
```

Затем выполните команду для обновления всех установленных пакетов до их последних версий:
```python
sudo apt upgrade
```
Эта команда может потребовать подтверждения перед началом обновления. Рекомендуем соглашаться с установкой всех обновлений, чтобы убедиться, что ваша система работает на последней версии программного обеспечения.

### Установка Docker
Чтобы установить Docker, воспользуйтесь инструкцией по установке с официального сайта:  
https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository    

### Установка Docker-compose
Чтобы установить Docker-compose, воспользуйтесь инструкцией по установке с официального сайта:
https://docs.docker.com/compose/install/

### Настройка файрвола
После установки Docker следующим важным шагом является настройка фаервола.  
Для веб-сервера, где используется Nginx, необходимо открыть порты 80 (HTTP) и 443 (HTTPS), чтобы клиенты могли подключаться к вашему приложению.

Для управления файрволом в Ubuntu используется утилита `ufw` (Uncomplicated Firewall).  

Сначала проверьте состояние файрвола с помощью команды:
```python
sudo ufw status
```
Если файрвол отключен, активируйте его:  
```python
sudo ufw enable
```
Теперь откройте необходимые порты:
Порт 80 для HTTP:
```python
sudo ufw allow 80/tcp
```

Порт 443 для HTTPS:
```python
sudo ufw allow 443/tcp
```
Чтобы обеспечить доступ к вашему серверу по SSH, необходимо оставить открытым порт 22:  
```python
sudo ufw allow 22/tcp
```

## Деплой и запуск  

При выполнении команды Git `Push` выполниться `workflow` GitHub Actions:  

- проверка линтером `flake8` и выполнение тестирования;
- создание образа проекта и пул на репозиторий DockerHub;
- сборка многоконтейнерного приложения на сервере.

## Команда проекта

- Dmitrii Grechko tg:@prime72rus
