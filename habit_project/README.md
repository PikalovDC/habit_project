# Habit Tracker

Трекер полезных привычек с Telegram-уведомлениями.

## Локальный запуск

1. Установи зависимости: `pip install -r requirements.txt`
2. Создай файл `.env` по примеру `.env.template` и заполни переменные
3. Выполни миграции: `python manage.py migrate`
4. Запусти сервер: `python manage.py runserver`

## Запуск через Docker Compose
`docker compose up -d --build`

## Переменные окружения

Создай файл `.env` со следующими переменными:
`SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-server-ip
NAME=habits
USER=tracker_user
PASSWORD=tracker_password
HOST=db
PORT=5432
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
TELEGRAM_BOT_TOKEN=your-telegram-token
EMAIL_HOST=smtp.yandex.ru
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_HOST_USER=your-email@yandex.ru
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=your-email@yandex.ru
CORS_ALLOWED_ORIGINS=http://localhost:3000
CSRF_TRUSTED_ORIGINS=http://localhost:3000`


## CI/CD

Проект использует GitHub Actions для автоматического тестирования и деплоя. При пуше в ветку main запускаются тесты, проверяется сборка Docker-образов, при успехе проект автоматически деплоится на сервер через SSH.

### Секреты GitHub для CI/CD

- SERVER_HOST - IP сервера
- SERVER_USER - пользователь SSH
- SSH_PRIVATE_KEY - приватный SSH-ключ
- SERVER_PORT - порт SSH (22)
- SECRET_KEY - секретный ключ Django

## Технологии

Django, DRF, PostgreSQL, Redis, Celery, Docker, Docker Compose, Telegram Bot API, GitHub Actions

## Документация API

- Swagger UI: /swagger/
- ReDoc: /redoc/

После запуска проекта документация доступна по адресам:

- Swagger UI: `http://127.0.0.1:8000/swagger/`
- ReDoc: `http://127.0.0.1:8000/redoc/`

Для просмотра документации на удаленном сервере замените `127.0.0.1` на IP вашего сервера.