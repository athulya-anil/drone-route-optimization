import six
import sys
sys.modules['kafka.vendor.six.moves'] = six.moves

import json
from kafka import KafkaConsumer

# Kafka Consumer setup
consumer = KafkaConsumer(
    "weather",
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

print("Listening for messages on 'weather'...")

for message in consumer:
    print(f"Received message: {message.value}")

