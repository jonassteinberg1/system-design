import boto3
import json
from faker import Faker
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the Faker library
fake = Faker()

# Initialize the boto3 client for SQS
sqs = boto3.client('sqs', region_name='us-west-2')

# Specify your SQS FIFO queue URL
queue_url = 'https://sqs.us-west-2.amazonaws.com/379683964026/fraud.fifo'

def generate_order(order_id):
    """Generate a fake order JSON object."""
    return {
        'order_id': order_id,
        'product_name': fake.word(),
        'product_id': fake.random_int(min=1000, max=9999),
        'quantity': fake.random_int(min=1, max=10),
        'date': fake.date(pattern="MM-DD-YYYY")
    }

def send_order_to_sqs(order):
    """Send an order to the SQS FIFO queue."""
    # Convert the order to a JSON string
    message_body = json.dumps(order)
    # The 'MessageGroupId' is required for FIFO queues. It's used to group messages together.
    # Here, using the order_id as part of the 'MessageDeduplicationId' to ensure uniqueness.
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message_body,
        MessageGroupId='orders_group'
    )
    logging.info(f"Sent order {order['order_id']} to SQS. Message ID: {response['MessageId']}")

def main():
    order_id = 1
    while True:
        order = generate_order(order_id)
        send_order_to_sqs(order)
        order_id += 1
        time.sleep(1)

if __name__ == "__main__":
    main()

