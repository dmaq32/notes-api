# Notes API

REST API для заметок: регистрация, вход по JWT и CRUD своих заметок. Создание и удаление заметки отправляют событие в RabbitMQ, отдельный воркер записывает его в таблицу `history`.

## Стек

- Python 3.12, FastAPI
- PostgreSQL 16, SQLAlchemy 2 (async), Alembic
- JWT (PyJWT), bcrypt
- RabbitMQ, aio-pika
- pytest
- Docker, Docker Compose

## Что умеет

- Регистрация и логин, пароль хранится в виде bcrypt-хеша
- Каждый пользователь видит и меняет только свои заметки
- Список заметок с пагинацией (`limit`, `offset`) и поиском по тексту (`filter`)
- Частичное обновление заметки через PATCH
- История событий `created` / `deleted` через очередь и отдельный воркер

## Запуск через Docker

```bash
git clone https://github.com/dmaq32/notes-api.git
cd notes-api
cp .env.example .env
docker compose up --build
```

Перед запуском заполни `.env`. Compose поднимает четыре контейнера: Postgres, RabbitMQ, API и воркер. Миграции применяются при старте API.

- Swagger: http://localhost:8000/docs
- Панель RabbitMQ: http://localhost:15672

## Переменные окружения

| Переменная | Пример |
|---|---|
| `POSTGRES_USER` | `postgres` |
| `POSTGRES_PASSWORD` | `postgres` |
| `POSTGRES_HOST` | `localhost` |
| `POSTGRES_PORT` | `5432` |
| `POSTGRES_DB` | `notes` |
| `JWT_SECRET` | любая длинная строка |
| `RABBITMQ_USER` | `guest` |
| `RABBITMQ_PASSWORD` | `guest` |
| `RABBITMQ_HOST` | `127.0.0.1` |
| `RABBITMQ_PORT` | `5672` |

`POSTGRES_HOST` и `RABBITMQ_HOST` нужны для локального запуска. Внутри Compose они заменяются на `db` и `rabbitmq`.

## Локальный запуск

Postgres и RabbitMQ в Docker, приложение из venv:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

docker compose up -d db rabbitmq
alembic upgrade head
uvicorn app.main:app --reload
```

Воркер запускается в отдельном терминале:

```bash
python -m app.rabbitmq.consumer
```

## Тесты

Тесты используют отдельную базу на том же Postgres. Её нужно создать один раз:

```sql
CREATE DATABASE "notes-api-tests";
```

```bash
pytest
```

В тестах RabbitMQ подменён моком, поэтому брокер для них не нужен.

## Эндпоинты

| Метод | Путь | Описание |
|---|---|---|
| GET | `/` | Проверка, что сервис жив |
| POST | `/users/register` | Регистрация |
| POST | `/users/login` | Логин, возвращает `access_token` |
| POST | `/notes/add_note` | Создать заметку |
| GET | `/notes/` | Свои заметки, параметры `limit`, `offset`, `filter` |
| GET | `/notes/{note_id}` | Одна заметка с email автора |
| PATCH | `/notes/{note_id}` | Изменить `text` и/или `is_done` |
| DELETE | `/notes/{note_id}` | Удалить заметку |

Эндпоинты `/notes` требуют заголовок `Authorization: Bearer <token>`.

Коды ответов: повторный email при регистрации даёт `409`, неверный токен `401`, чужая или несуществующая заметка `404`.

## Структура

```
app/
  main.py          # приложение, lifespan с подключением к RabbitMQ
  utils.py         # JWT и получение текущего пользователя
  routers/         # ручки users и notes
  db/              # модели, схемы, подключение к базе
  rabbitmq/        # настройки брокера и воркер
alembic/           # миграции
tests/             # pytest
```
