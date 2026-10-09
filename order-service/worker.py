import time
import random

def process_payment(order_id: int):
    print(f"Processing payment for Order #{order_id}...")
    time.sleep(1.5) # Simulate external payment gateway latency
    if random.choice([True, True, False]): # 66% success rate simulation
        print(f"Payment SUCCESS for Order #{order_id}")
    else:
        print(f"Payment FAILED for Order #{order_id} - Initiating refund workflow")

if __name__ == "__main__":
    print("Billing Worker started, listening for events...")
    while True:
        time.sleep(5)