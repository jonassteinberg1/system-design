from kafka import KafkaConsumer
import json
import time

def create_consumer():
    return KafkaConsumer(
        'topic1',
        bootstrap_servers='kafka:9092',
        auto_offset_reset='earliest',
        group_id='subscriber1-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

def consume_messages(consumer, run_time=30):
    start_time = time.time()
    for message in consumer:
        print(f"Subscriber 1 Consumed: {message.value}")
        if time.time() - start_time > run_time:
            break

while True:
    consumer = create_consumer()
    consume_messages(consumer)
    consumer.close()
    time.sleep(10)

