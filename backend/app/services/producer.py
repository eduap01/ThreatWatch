import json
import os


from aio_pika import connect_robust, Message
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL","amqp://guest:guest@localhost/")

async def send_analysis_task(task_data: dict):
    connection = await connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue_name = "file_analysis"

        await channel.declare_queue(queue_name, durable=True)

        message = Message(
            body=json.dumps(task_data).encode(),
            content_type="application/json"
        )

        await channel.default_exchange.publish(
            message, routing_key=queue_name
        )

        print(f"Task sent to RabbitMQ: {task_data}")