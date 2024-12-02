import six
import sys
sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaConsumer
import json

# Kafka consumer
consumer = KafkaConsumer(
    'airspace',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Listening for messages on 'airspace'...")

for message in consumer:
    print(f"Received message: {message.value}")

