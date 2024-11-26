from utils.rbmq_connect import rbmq_mn, send_message
from db.repository import Repository
from db.connection import Session
from aio_pika import Message
import asyncio
from asyncio import sleep
import json
from random import randint
from utils.log import get_logger

from config import AMQP


class Scheduler:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.rep = Repository(Session)
        self.connection = None
        self.channel = None
        self.resp_queues = {
            AMQP['work_queue']: self.on_message_scheduler
        }

    async def connect(self):
        self.logger.info('connect')
        self.connection = await rbmq_mn()
        self.channel = await self.connection.channel()
        self.logger.info('connected')
        return self

    async def on_message_scheduler(self, message: Message):
        async with message.process():
            self.logger.info(message.body)
            body = json.loads(message.body)
            reply_to = message.reply_to
            if 'params' in body and body['params']=='new_task':
                body.pop('params')
                self.rep.create_task(**body)
            elif 'params' in body and body['params']=='processing':
                body.pop('params')
                await sleep(randint(2, 5))
                chance = randint(0, 100)
                if chance > 50:
                    body['status'] = 'complete'
                else:
                    body['status'] = 'error'
                await send_message(body, AMQP['resp_queue'], reply_to=reply_to)


            # message.ack()

    async def consume(self):
        for queue, on_message in self.resp_queues.items():
            queue = await self.channel.declare_queue(queue, durable=True)
            await queue.consume(on_message)

if __name__ == '__main__':
    sch = Scheduler()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sch.connect())
    loop.run_until_complete(sch.consume())
    loop.run_forever()
