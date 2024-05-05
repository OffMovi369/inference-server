import asyncio
from propan import PropanApp, RabbitBroker
from propan.brokers.rabbit import RabbitExchange, RabbitQueue, ExchangeType
import cv2 as cv


broker = RabbitBroker("amqp://localhost:5672")
app = PropanApp(broker)

exchange = RabbitExchange("test-exchange", type=ExchangeType.DIRECT)

response_queue = RabbitQueue("response-q")

current_frame = None
current_car_list = []

def generate_frame(frame, car_list:list):
    for box in car_list:
        label = box[0]
    
        cv.rectangle(frame, box[1:], (0,0,255), 2)
        cv.putText(frame, label, (box[1], box[2]-10), cv.FONT_HERSHEY_COMPLEX, 0.3, (0,0,255), 1)
    
    # cv.imshow('frame', frame)
    return frame

# def check_process(p):
#     if not p.is_alive():
#         print("PROc died")

# def new_process(frame, message):
#     p = mp.Process(target=show_frame, args=(frame, message))
#     p.start()
#     check_process(p)

@broker.handle(response_queue, exchange)
async def handle_response(message):
    frame = generate_frame(current_frame, message)    
    cv.imshow('frame', frame)
    cv.waitKey(0)

async def send_image(file_name: str) -> None:
    global current_frame
    current_frame = cv.imread(file_name)
    _, img_arr = cv.imencode(".jpeg", img = current_frame)

    await broker.publish(message=img_arr.tobytes(), exchange=exchange, routing_key="request-q")

async def send_video(file_name: str) -> None:
    global current_frame
    
    cap = cv.VideoCapture(file_name)

    while(cap.isOpened()):
        
        ret, frame = cap.read()
        
        if ret:
            _, arr_frame = cv.imencode('.jpeg', frame)
            bytes_frame = arr_frame.tobytes()
            await broker.publish(message=bytes_frame, exchange=exchange, routing_key="request-q")

        current_frame = generate_frame(frame, current_car_list)
        
        cv.imshow('frame', current_frame)
        
        key = cv.waitKey(1)
        if key == ord('q'):
            break

@app.after_startup
async def main():
    await send_image("example.jpeg")
    # await send_video("example.avi")
  
if __name__ == "__main__":
    asyncio.run(app.run())