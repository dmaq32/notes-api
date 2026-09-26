# Notes API
Заметки пользователя. FastAPI, PostgreSQL, Alembic, RabbitMQ.
## Запуск

```bash
git clone https://github.com/dmaq32/notes-api.git
cd notes-api
python3 -m venv venv
#MacOS & Linux
source venv/bin/activate
pip install -r requirements.txt
```

Скопируй `.env.example` в `.env` и заполни `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `JWT_SECRET`. Хост — `localhost`, порт `5432`.

Postgres и RabbitMQ:

```bash
docker compose up -d
alembic upgrade head
uvicorn app.main:app --reload
```

Панель RabbitMQ: http://localhost:15672 , логин и пароль `guest`.

Воркер истории запускается отдельно, из того же venv:

```bash
python -m app.rabbitmq.consumer
```

Создание заметки пишет строку в `notes` и кладёт в очередь событие с `note_id`, `user_id` и `created`. Воркер дописывает это в таблицу `history`.

Тестовая база на том же Postgres. Имя с дефисами, в кавычках:

```sql
CREATE DATABASE "notes-api-tests";
```

Тесты: pytest tests/test_api.py

## Ручки

- `GET /` — статус сервиса.
- `POST /users/register` — имя, email, пароль. Пароль хранится как хеш.
- `POST /users/login` — email и пароль, в ответе access_token.
- Дальше заголовок `Authorization: Bearer <токен>`.
- `POST /notes/add_note` — создать заметку, в теле только text.
- `GET /notes/` — свои заметки. Параметры limit, offset и filter по тексту.
- `GET /notes/{note_id}` — одна своя заметка и email автора.
- `PATCH /notes/{note_id}` — изменить text и is_done, можно прислать только одно поле.
- `DELETE /notes/{note_id}` — удалить свою заметку.
- Чужая или несуществующая заметка — 404. Неверный токен — 401.
