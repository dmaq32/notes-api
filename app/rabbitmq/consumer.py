from app.rabbitmq.config import QUEUE_NAME, create_connection, EXCHANGE_NAME, EXCHANGE_TYPE, EXCHANGE_DURABLE
from sqlalchemy import insert
from app.db.models import History
import json
import asyncio
from app.db.config import AsyncSessionLocal
import logging

async def callback(message):
    try:
        data = json.loads(message.body.decode())
        note_id, user_id, event = data["note_id"], data["user_id"], data["event"]

        async with AsyncSessionLocal() as session:
            async with session.begin():
                await session.execute(
                    insert(History).values(
                        note_id=note_id,
                        user_id=user_id,
                        event=event,
                    )
                )

        logging.info(f" [x] Received {message.body}")
        await message.ack()

    except Exception as e:
        logging.error(f" [x] Error: {e}")
        await message.reject(requeue=True)
    return event


async def consume():
    connection = await create_connection()
    async with connection.channel() as channel:

        notes_exchange = await channel.declare_exchange(
            EXCHANGE_NAME,
            type=EXCHANGE_TYPE,
            durable=EXCHANGE_DURABLE,
        )
        create_queue = await channel.declare_queue(
            QUEUE_NAME["created"],
            durable=True,
            arguments={"x-queue-type": "quorum"},
        )
        logging.info(f" [x] Queue declared: {create_queue}")
        delete_queue = await channel.declare_queue(
            QUEUE_NAME["deleted"],
            durable=True,
            arguments={"x-queue-type": "quorum"},
        )
        logging.info(f" [x] Queue declared: {delete_queue}")

        await create_queue.bind(exchange=EXCHANGE_NAME, routing_key=QUEUE_NAME["created"])
        await delete_queue.bind(exchange=EXCHANGE_NAME, routing_key=QUEUE_NAME["deleted"])


        await create_queue.consume(callback=callback)
        await delete_queue.consume(callback=callback)
        await asyncio.Future()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(consume())
