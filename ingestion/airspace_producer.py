import six
import sys
sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaProducer
import json
import time
import requests

# Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Mock API URL for airspace data
MOCK_URL = "https://run.mocky.io/v3/23d5d6e4-4ce4-45bf-8f18-4bbbb6712528"

while True:
    try:
        # Fetch airspace data from the mock API
        response = requests.get(MOCK_URL)
        if response.status_code == 200:
            airspace_data = response.json()
            # Send the data to the Kafka topic 'airspace'
            producer.send('airspace', value=airspace_data)
            print(f"Sent to 'airspace': {airspace_data}")
        else:
            print(f"Failed to fetch data: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(10)  # Fetch data every 10 seconds

