#  Трекер полезных привычек (Habit Tracker)

Бэкенд-часть SPA веб-приложения для отслеживания полезных привычек, вдохновленного книгой Джеймса Кира "Атомные привычки".

##  Описание проекта

Приложение позволяет пользователям создавать и отслеживать полезные привычки, привязывать к ним приятные привычки в качестве вознаграждения, устанавливать расписание выполнения и получать напоминания через Telegram-бота.

### Ключевые возможности:

-  Создание полезных и приятных привычек
-  Привязка вознаграждений или связанных привычек
-  Настройка расписания и периодичности выполнения
-  Автоматические напоминания через Telegram (Celery + Celery Beat)
-  Публичный доступ к привычкам (можно делиться примерами)
-  Безопасная JWT-авторизация
-  Пагинация списков
-  Автоматическая генерация документации API (Swagger/ReDoc)

---

##  Технологический стек

- **Python 3.12**
- **Django 4.2** — веб-фреймворк
- **Django REST Framework** — создание REST API
- **Simple JWT** — JWT-аутентификация
- **PostgreSQL** — реляционная база данных
- **Redis** — брокер сообщений для Celery
- **Celery** — очередь задач
- **Celery Beat** — планировщик задач
- **Telegram Bot API** — отправка уведомлений
- **pytest** — тестирование
- **drf-spectacular** — генерация OpenAPI документации
- **django-environ** — управление переменными окружения

---

##  Требования к окружению

Перед началом работы убедитесь, что у вас установлены:

- Python 3.10+
- PostgreSQL 14+
- Redis 6.0+
- pip (менеджер пакетов Python)

---

##  Установка и запуск

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd PythonProject15

python -m venv venv

2. Windows:
venv\Scripts\activate

macOS/Linux:
source venv/bin/activate

3. Установка зависимостей
pip install -r requirements.txt

4. Настройка переменных окружения
Скопируйте файл .env.template в .env и заполните реальные значения:

4. Настройка переменных окружения
Скопируйте файл .env.template в .env и заполните реальные значения:

cp .env.template .env

Откройте .env и настройте:

DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# База данных PostgreSQL
DB_NAME=habits_db
DB_USER=postgres
DB_PASSWORD=your_db_password
DB_HOST=127.0.0.1
DB_PORT=5432

# CORS (домен фронтенда)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Celery & Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

5. Создание базы данных PostgreSQL
Подключитесь к PostgreSQL и создайте базу данных:

CREATE DATABASE habits_db;

6. Применение миграций

python manage.py makemigrations
python manage.py migrate

7. Создание суперпользователя (опционально)

python manage.py createsuperuser

8. Запуск сервера разработки

python manage.py runserver

Сервер будет доступен по адресу: http://127.0.0.1:8000/

 Запуск Celery (для отправки уведомлений)
1. Убедитесь, что Redis запущен
Windows (Docker):

docker run -d -p 6379:6379 redis

macOS/Linux:

sudo systemctl start redis

2. Запуск Celery Worker

celery -A config worker --loglevel=info --pool=solo

3. Запуск Celery Beat (планировщик)
Откройте третий терминал и выполните:

celery -A config beat --loglevel=info

Теперь задачи будут запускаться автоматически по расписанию (каждую минуту).

Запуск тестов

pytest

Для просмотра отчета о покрытии в HTML-формате:

pytest --cov=habits --cov-report=html

Откройте файл htmlcov/index.html в браузере.

Документация API

После запуска сервера документация API доступна по адресам:
Swagger UI: http://127.0.0.1:8000/api/docs/
ReDoc: http://127.0.0.1:8000/api/redoc/
OpenAPI Schema: http://127.0.0.1:8000/api/schema/

Основные эндпоинты API

Аутентификация

Метод
Эндпоинт
Описание
POST
/api/token/
Получение JWT токенов (login)
POST
/api/token/refresh/
Обновление access токена

Привычки

Метод
Эндпоинт
Описание
GET
/api/habits/my/
Список привычек текущего пользователя (с пагинацией)
POST
/api/habits/my/
Создание новой привычки
GET
/api/habits/my/{id}/
Получение конкретной привычки
PUT
/api/habits/my/{id}/
Полное обновление привычки
PATCH
/api/habits/my/{id}/
Частичное обновление привычки
DELETE
/api/habits/my/{id}/
Удаление привычки
GET
/api/habits/public/
Список публичных привычек (только чтение)

PythonProject15/
├── config/
│   ├── __init__.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── habits/
│   ├── migrations/
│   ├── conftest.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tasks.py
│   ├── test_models.py
│   ├── test_views.py
│   ├── urls.py
│   └── views.py
├── .dockerignore          
├── .env                   
├── .env.template          
├── .gitignore
├── Dockerfile            
├── docker-compose.yml     
├── manage.py
├── pytest.ini
├── README.md              
└── requirements.txt

Безопасность

Все секретные данные (ключи, пароли, токены) хранятся в файле .env
Файл .env добавлен в .gitignore и не попадает в репозиторий
Используется JWT-аутентификация с ограниченным временем жизни токенов
CORS настроен для работы с конкретными доменами фронтенда
Права доступа контролируются на уровне ViewSet (владелец может редактировать только свои привычки)

Бизнес-логика и валидаторы

Модель Habit (Привычка)
Поля модели:
user — создатель привычки
place — место выполнения
time — время выполнения
action — действие (сама привычка)
is_pleasant — признак приятной привычки
associated_habit — связанная привычка (вознаграждение)
periodicity — периодичность выполнения (в днях)
reward — вознаграждение (строка)
execution_time — время на выполнение (в секундах)
is_public — признак публичности

Валидаторы
Нельзя одновременно указывать вознаграждение и связанную привычку
Время выполнения не должно превышать 120 секунд
В связанные привычки могут попадать только приятные привычки
У приятной привычки не может быть вознаграждения или связанной привычки
Нельзя выполнять привычку реже, чем 1 раз в 7 дней

##  Запуск через Docker Compose (рекомендуется)

### Требования

- Docker Desktop (Windows/macOS) или Docker Engine (Linux)
- Docker Compose v2+

### Быстрый старт

#### 1. Склонируйте репозиторий

```bash
git clone <repository-url>
cd PythonProject15

Настройте переменные окружения
cp .env.template .env

Откройте .env и заполните:
SECRET_KEY — любой случайный набор символов
DB_PASSWORD — пароль для PostgreSQL
TELEGRAM_BOT_TOKEN — токен от @BotFather
TELEGRAM_CHAT_ID — ваш числовой ID в Telegram

Запустите все сервисы одной командой
docker-compose up --build -d


