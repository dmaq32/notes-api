import pika
from app.db.config import build_database_url
from sqlalchemy import create_engine

engine_rabbit = create_engine(build_database_url("psycopg2"))
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='test_queue', durable=True, arguments={'x-queue-type': 'quorum'})

