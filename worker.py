# get tasks from db, create task from message

from aio_pika import Message
from config import AMQP
from db.repository import Repository
from db.connection import Session
from utils.log import get_logger
from utils.rbmq_connect import rbmq_mn, send_message
import json
import asyncio

from utils.planner import planner
from amqp.utils import serialize

class Worker:
    def __init__(self):
        self.logger = get_logger('worker')
        self.rep = Repository(Session)
        self.connection = None
        self.channel = None
        self.resp_queues = {AMQP['resp_queue']: self.on_message_worker}

    async def connect(self):
        try:
            self.connection = await rbmq_mn()
            self.channel = await self.connection.channel()
        except Exception as e:
            self.logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    @planner(1)
    async def send_tasks(self):
        tasks = self.rep.get_tasks('desc',status='created')
        for task in tasks:
            body = serialize(task.__dict__)
            body['params'] = 'processing'
            self.logger.debug(body)
            try:
                await send_message(
                    queue=AMQP['work_queue'],
                    body=body,
                    reply_to=AMQP['resp_queue'],
                    durable=True
                )
                self.rep.update_status_task(stage='proc', id=task.id)
            except Exception as e:
                self.logger.error(f"Error sending task: {e}")

    async def on_message_worker(self, message: Message):
        async with message.process():
            try:
                self.logger.info(message.body)
                body = json.loads(message.body)
                self.rep.update_status_task(stage=body['status'], id=body['id'])
            except Exception as e:
                self.logger.error(f"Error processing message: {e}")

    async def consume(self):
        if not self.channel:
            self.logger.error("Channel is not initialized. Exiting consume.")
            return
        for queue_name, on_message in self.resp_queues.items():
            try:
                self.logger.info(f"Declaring queue: {queue_name}")
                queue = await self.channel.declare_queue(queue_name, durable=False)
                await queue.consume(on_message)
            except Exception as e:
                self.logger.error(f"Error consuming from queue {queue_name}: {e}")



if __name__ == '__main__':
    mn = Worker()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def main():
        try:
            await mn.connect()
            consume_task = loop.create_task(mn.consume())
            send_task = loop.create_task(mn.send_tasks())
            await asyncio.gather(consume_task, send_task)
        except Exception as e:
            mn.logger.error(f"Error in main tasks: {e}")
            raise

    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Caught keyboard interrupt. Cancelling tasks...")
    finally:
        pending_tasks = asyncio.all_tasks(loop)
        for task in pending_tasks:
            task.cancel()
        loop.run_until_complete(asyncio.gather(*pending_tasks, return_exceptions=True))
        
        if mn.connection:
            loop.run_until_complete(mn.connection.close())
        
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

