import boto3
import json
import logging
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the boto3 client for SQS
sqs = boto3.client('sqs', region_name='us-west-2')

# Specify your SQS FIFO queue URLs
orders_queue_url = 'https://sqs.us-west-2.amazonaws.com/379683964026/fraud.fifo'
payments_queue_url = 'https://sqs.us-west-2.amazonaws.com/379683964026/payments.fifo'

def receive_message_from_orders():
    try:
        # Receive a message from the Orders FIFO queue
        response = sqs.receive_message(
            QueueUrl=orders_queue_url,
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

def process_and_send_to_payments(message):
    # Parse the message body
    body = json.loads(message['Body'])
    order_id = body['order_id']
    
    # Perform fraud check
    fraud_check_result = 'passed' if order_id % 2 == 0 else 'failed'
    body['fraud_check'] = fraud_check_result
    
    # Send the modified message to the Payments FIFO queue
    response = sqs.send_message(
        QueueUrl=payments_queue_url,
        MessageBody=json.dumps(body),
        MessageGroupId='payments_group',
    )
    logging.info(f"Sent fraud_check {body['order_id']} to SQS. Message ID: {response['MessageId']}")
    
    # Delete the processed message from Orders queue
    #try:
    #    sqs.delete_message(
    #        QueueUrl=orders_queue_url,
    #        ReceiptHandle=message['ReceiptHandle']
    #    )
    #    logging.info(f"Message with ReceiptHandle {message['ReceiptHandle']} deleted successfully.")
    #except Exception as e:
    #    # Log any exceptions during message deletion
    #    logging.error(f"Failed to delete message with ReceiptHandle {{message['ReceiptHandle']}}. Error: {e}")
    sqs.delete_message(
        QueueUrl=orders_queue_url,
        ReceiptHandle=message['ReceiptHandle']
    )

def main():
    while True:
        message = receive_message_from_orders()
        if message:
            process_and_send_to_payments(message)
        else:
            logging.info("No messages to process. Waiting...")

if __name__ == "__main__":
    main()

