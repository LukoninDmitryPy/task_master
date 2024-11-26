from aio_pika import connect as cn, Message
from config import AMQP
import json

async def rbmq_mn():
    connection = await cn(
            host=AMQP['host'],
            port=AMQP['port'],
            login=AMQP['user'],
            password=AMQP['pass']
        )
    return connection

async def send_message(body, queue, connection=None, ch=None, reply_to=None, durable=False, exp=None):
    connection = await rbmq_mn() if connection is None else connection
    async with connection:
        ch = await connection.channel() if ch is None else ch
        await ch.declare_queue(name=queue, durable=durable)
        await ch.default_exchange.publish(Message(
            json.dumps(body).encode(),
            content_type="application/json",
            expiration=exp,
            reply_to=reply_to
        ), routing_key=queue)