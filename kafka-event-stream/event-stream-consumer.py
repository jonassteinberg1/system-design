from kafka import KafkaConsumer, TopicPartition
import json
import sys
import time

consumer = KafkaConsumer(
    bootstrap_servers=['kafka:9092'],
    #auto_offset_reset='earliest',  # Start from the earliest message
    #enable_auto_commit=False,     # Disable auto commit to manually manage offsets
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id='event-stream-consumer',
    fetch_max_wait_ms=500
)

topic = 'event-stream-topic'
consumer.subscribe([topic])

# Function to process messages
def process_messages(limit=None):
    count = 0
    start_time = time.time()
    for message in consumer:
        print(f"Consumed: {message.value}")
        # Committing the offset after message is processed
        sys.stdout.flush()
        consumer.commit()
        count += 1
        if limit and count >= limit:
            break
        if time.time() - start_time > 60:
            break

# Consume and process messages normally
print("Consuming messages...")
process_messages(limit=100)

#Optional: Replay messages
#Uncomment the lines below to enable replay functionality
print("Replaying messages...")
consumer.seek_to_beginning()
process_messages()

