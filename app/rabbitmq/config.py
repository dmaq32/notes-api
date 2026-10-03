import os

import aio_pika
from aio_pika import ExchangeType
from dotenv import load_dotenv

load_dotenv()

EXCHANGE_NAME = "notes"
EXCHANGE_TYPE = ExchangeType.DIRECT
EXCHANGE_DURABLE = True

QUEUE_NAME = {
    "created": "note.created",
    "deleted": "note.deleted",
}


async def create_connection():
    user = os.environ["RABBITMQ_USER"]
    password = os.environ["RABBITMQ_PASSWORD"]
    host = os.environ["RABBITMQ_HOST"]
    port = os.environ["RABBITMQ_PORT"]
    return await aio_pika.connect_robust(
        f"amqp://{user}:{password}@{host}:{port}/",
    )
