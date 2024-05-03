import asyncio
from propan import PropanApp, RabbitBroker
from propan.brokers.rabbit import RabbitExchange, RabbitQueue, ExchangeType
import cv2 as cv

broker = RabbitBroker("amqp://localhost:5672")
app = PropanApp(broker)

exchange = RabbitExchange("test-exchange", type=ExchangeType.DIRECT)

response_queue = RabbitQueue("response-q")

global_frame = cv.imread("example.jpeg")

def show_frame(frame, car_list:list):
    for box in car_list:
        label = box[0]
    
        cv.rectangle(frame, box[1:], (0,0,255), 2)
        cv.putText(frame, label, (box[1], box[2]-10), cv.FONT_HERSHEY_COMPLEX, 0.3, (0,0,255), 1)
    
    cv.imshow('frame', frame)
    cv.waitKey(0)

@broker.handle(response_queue, exchange)
async def handle_response(message):
    print("from server ->", type(message))
    show_frame(global_frame, message)

@app.after_startup
async def send_message():
    with open("example.jpeg", "rb") as fl:
        await broker.publish(message=fl.read(), exchange=exchange, routing_key="request-q")

if __name__ == "__main__":
    asyncio.run(app.run())