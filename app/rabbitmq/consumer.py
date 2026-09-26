from app.rabbitmq.config import channel, engine_rabbit
from sqlalchemy import insert
from app.db.models import History
import json

def callback(ch, method, properties, body):
    with engine_rabbit.begin() as conn:
        data = json.loads(body)
        note_id, user_id, event = data["note_id"], data["user_id"], data["event"]
        conn.execute(insert(History).values(note_id=note_id, user_id=user_id, event=event))
        print(f" [x] Received {body}")
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(queue='test_queue', on_message_callback=callback)
try:
    channel.start_consuming()
finally:
    channel.close()