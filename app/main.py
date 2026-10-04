from fastapi import FastAPI
from app.routers import note_router, user_router
from app.rabbitmq.config import (
    create_connection,
    EXCHANGE_NAME,
    EXCHANGE_TYPE,
    EXCHANGE_DURABLE,
)

from dotenv import load_dotenv
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import logging

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    connection = await create_connection()
    logging.info(f" [x] Connection: {connection}")
    app.state.connection = connection

    channel = await connection.channel()
    app.state.channel = channel
    logging.info(f" [x] Channel: {channel}")

    notes_exchange = await channel.declare_exchange(
        EXCHANGE_NAME,
        type=EXCHANGE_TYPE,
        durable=EXCHANGE_DURABLE,
    )
    app.state.notes_exchange = notes_exchange
    logging.info(f" [x] Notes exchange: {notes_exchange}")

    try:
        yield
    finally:
        logging.info(f" [x] Closing connection and channel")
        await connection.close()
        await channel.close()


app = FastAPI(lifespan=lifespan)
app.include_router(note_router)
app.include_router(user_router)

@app.get("/")
def health():
    return {"status": "ok"}
