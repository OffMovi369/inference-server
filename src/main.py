import asyncio
from propan import PropanApp, RabbitBroker
from propan.brokers.rabbit import RabbitExchange, RabbitQueue, ExchangeType
import numpy as np
import cv2
from detector import get_car_list

# Объявление брокера и самого приложения
broker = RabbitBroker("amqp://localhost:5672")
app = PropanApp(broker)

# Определение обменника, его типа
exchange = RabbitExchange("test-exchange", type=ExchangeType.DIRECT)

request_queue = RabbitQueue("request-q")

@broker.handle(request_queue, exchange)
async def handle_request(message: bytes):
    # Перевод байтов в данные для opencv
    img_array = cv2.imdecode(np.frombuffer(message, dtype=np.uint8), -1)
    out = get_car_list(img_array)
    
    await broker.publish(message=out, exchange=exchange, routing_key="response-q")

# @app.after_startup
# async def send_messages():
	
#     await broker.publish(message="test", exchange=exchange, routing_key="test-q-1")

# 	await broker.publish(exchange=exchange, routing_key="test-q-2")

if __name__ == "__main__":
    asyncio.run(app.run())