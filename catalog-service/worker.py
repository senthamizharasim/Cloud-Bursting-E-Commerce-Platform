import pika
import json

def callback(ch, method, properties, body):
    order = json.loads(body)
    print(f"[+] Processing Order: Deducting {order['quantity']} of Product ID {order['product_id']}")

connection = pika.BlockingConnection(pika.ConnectionParameters('host.minikube.internal'))
channel = connection.channel()
channel.queue_declare(queue='order_queue')

channel.basic_consume(queue='order_queue', on_message_callback=callback, auto_ack=True)

print('[*] Waiting for orders. Press CTRL+C to exit')
channel.start_consuming()