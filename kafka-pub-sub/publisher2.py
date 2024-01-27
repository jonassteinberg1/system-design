from kafka import KafkaProducer
import json
import time

def create_producer():
    return KafkaProducer(
        bootstrap_servers='kafka:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def publish_messages(producer, topic):
    for i in range(1000):
        message = {'publisher': 'publisher2', 'message': f'Message {i} from publisher 2'}
        producer.send(topic, value=message)
        print(f"Sent: {message}")
        time.sleep(1)

producer = create_producer()
publish_messages(producer, 'topic2')
producer.close()

