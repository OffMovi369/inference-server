import asyncio
from propan import PropanApp, RabbitBroker
from propan.brokers.rabbit import RabbitExchange, RabbitQueue, ExchangeType

broker = RabbitBroker("amqp://localhost:5672")
app = PropanApp(broker)

exchange = RabbitExchange("test-exchange", type=ExchangeType.DIRECT)

response_queue = RabbitQueue("response-q")

@broker.handle(response_queue, exchange)
async def handle_response(message):
    print("handler1", message)

@app.after_startup
async def send_messages():
    with open("example.jpeg", "rb") as fl:
        await broker.publish(message=fl.read(), exchange=exchange, routing_key="request-q")

if __name__ == "__main__":
    asyncio.run(app.run())