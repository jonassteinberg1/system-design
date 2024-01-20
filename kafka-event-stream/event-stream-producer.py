from kafka import KafkaProducer
import json
import sys
import time

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'event-stream-topic'

for i in range(100):
    message = {'event': f'Event {i}'}
    producer.send(topic, value=message)
    print(f"Produced: {message}")
    sys.stdout.flush() # Flush python buffer so that consumer logs immediately
    time.sleep(1)

producer.close()

