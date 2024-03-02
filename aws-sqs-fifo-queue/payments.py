import boto3
import json
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the boto3 client for SQS
sqs = boto3.client('sqs', region_name='us-west-2')

# Specify your SQS FIFO queue URL
queue_url = 'https://sqs.us-west-2.amazonaws.com/379683964026/payments.fifo'

def receive_message_from_payments():
    try:
        # Receive a message from the Orders FIFO queue
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['SentTimestamp'],
            MaxNumberOfMessages=1,
            MessageAttributeNames=['All'],
            VisibilityTimeout=30,  # Time the message is invisible to other consumers
            WaitTimeSeconds=0  # Use long polling
        )

        # Check if message is received
        if 'Messages' in response:
            return response['Messages'][0]  # Return the first message
        else:
            return None
    except NoCredentialsError:
        logging.info("Credentials not available.")
        return None
    except PartialCredentialsError:
        logging.info("Partial credentials provided, check your configuration.")
        return None

def process_payments(message):
    # Parse the message body
    body = json.loads(message['Body'])

    # Perform fraud check
    fraud_check_result = body['fraud_check']
    if fraud_check_result is 'passed':
        logging.info(f"fraud_check for {body['order_id']} passed")
    else:
        logging.info(f"fraud_check for {body['order_id']} failed")

    try:
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=message['ReceiptHandle']
        )
        logging.info(f"Message with ReceiptHandle {message['ReceiptHandle']} deleted successfully.")
    except Exception as e:
        # Log any exceptions during message deletion
        logging.error(f"Failed to delete message with ReceiptHandle {{message['ReceiptHandle']}}. Error: {e}")

def main():
    while True:
        message = receive_message_from_payments()
        if message:
            process_payments(message)
        else:
            logging.info("No messages to process. Waiting...")

if __name__ == "__main__":
    main()
