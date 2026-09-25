# Notes API
Заметки пользователя. FastAPI, PostgreSQL, Alembic.
## Запуск

```bash
python3 -m venv venv
#MacOS & Linux
source venv/bin/activate
pip install -r requirements.txt
```

Скопируй `.env.example` в `.env` и заполни `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `JWT_SECRET`. Эти значения должны совпадать с поднятым Postgres.


Postgres в Docker. Пользователь, пароль и база в команде те же, что в `.env`. Хост в `.env` — `localhost`, порт `5432`.

```bash
docker run --name notes-db --env-file .env -p 5432:5432 -d postgres:16
alembic upgrade head
uvicorn app.main:app --reload
```

Тесты: pytest tests/test_api.py

## Ручки

GET / — статус сервиса.
POST /users/register — имя, email, пароль. Пароль хранится как хеш.
POST /users/login — email и пароль, в ответе access_token.
Дальше заголовок Authorization: Bearer <токен>.
POST /notes/add_note — создать заметку, в теле только text.
GET /notes/ — свои заметки. Параметры limit, offset и filter по тексту.
GET /notes/{note_id} — одна своя заметка и email автора.
PATCH /notes/{note_id} — изменить text и is_done, можно прислать только одно поле.
DELETE /notes/{note_id} — удалить свою заметку.
Чужая или несуществующая заметка — 404. Неверный токен — 401.