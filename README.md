# Notes API

Заметки пользователя. FastAPI, async SQLAlchemy 2, PostgreSQL 16, Alembic, JWT, RabbitMQ, pytest.

Регистрация и логин, свои заметки, журнал событий в `history` через очередь.

## Запуск через Docker Compose

Скопируй `.env.example` в `.env` и заполни все переменные.  
Для локального `uvicorn` оставь `POSTGRES_HOST=localhost` и `RABBITMQ_HOST=127.0.0.1`.  
В Compose у `api` и `worker` хосты подменяются на имена сервисов `db` и `rabbitmq`. Логин и пароль брокера берутся из `.env`.

```bash
git clone https://github.com/dmaq32/notes-api.git
cd notes-api
cp .env.example .env
# заполни .env
docker compose up --build
```

Поднятся Postgres, RabbitMQ, API и воркер.  
API: http://127.0.0.1:8000  
Панель RabbitMQ: http://localhost:15672 , логин и пароль из `.env` (`RABBITMQ_USER` / `RABBITMQ_PASSWORD`).

Миграции на старте API: `alembic upgrade head`.  
Воркер — отдельный контейнер с командой `python -m app.rabbitmq.consumer`.

Создание и удаление заметки пишут в Postgres и публикуют в обмен `notes` события `note.created` и `note.deleted`. Воркер пишет строку в `history`.

## Локальный запуск без контейнеров API/worker

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
docker compose up -d db rabbitmq
alembic upgrade head
uvicorn app.main:app --reload
python -m app.rabbitmq.consumer
```

## Тесты

На том же Postgres отдельная база:

```sql
CREATE DATABASE "notes-api-tests";
```

```bash
pytest tests/test_api.py
```

Тесты ходят в `notes-api-tests`. RabbitMQ в тестах подменён: брокер для `pytest` не нужен.

## Ручки

- `GET /` — статус сервиса.
- `POST /users/register` — имя, email, пароль. Пароль хранится как хеш. Повторный email — `409`.
- `POST /users/login` — email и пароль, в ответе `access_token`.
- Дальше заголовок `Authorization: Bearer <токен>`.
- `POST /notes/add_note` — создать заметку, в теле только `text`, `201`.
- `GET /notes/` — свои заметки. Параметры `limit`, `offset` и `filter` по тексту.
- `GET /notes/{note_id}` — одна своя заметка и email автора (JOIN).
- `PATCH /notes/{note_id}` — изменить `text` и `is_done`, можно прислать только одно поле.
- `DELETE /notes/{note_id}` — удалить свою заметку, `204`.
- Чужая или несуществующая заметка — `404`. Неверный токен — `401`.
