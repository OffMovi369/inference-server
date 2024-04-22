# import pika
# import sys
# import os

# connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
# channel = connection.channel()

# # Определяем очередь, в которую будет доставлено сообщение
# channel.queue_declare('test')

# # base64.b64decode(fl.read())

# def main():
#     while True:
#         data = input('[*] Enter sent data: ')
#         channel.basic_publish(exchange='', routing_key='test', body=data)
        
#         print(f"[x] Sent '{data}' ")

# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         print('Interrupted')
        
#         try:
#             sys.exit(0)
#         except SystemExit:
#             os._exit(0)
#     finally:
#         connection.close()