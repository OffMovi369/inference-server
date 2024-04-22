import pika
import os
import sys
import base64

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()

channel.queue_declare('media')

def callback(ch, method, properties, body):
    img_bytes = base64.decode(body)
    # prototype
    # car_list = detector.detect()
    # sender.send()

channel.basic_consume(queue='test',
                    auto_ack=True,
                    on_message_callback=callback)

def main():
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)