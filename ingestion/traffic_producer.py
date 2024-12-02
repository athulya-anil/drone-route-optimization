import six
import sys
sys.modules['kafka.vendor.six.moves'] = six.moves

import time
import json
import requests
from kafka import KafkaProducer

# Kafka Producer setup
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Mock API URL
MOCK_URL = "https://run.mocky.io/v3/ad54a600-8f2e-4f60-a455-45ca44d09f21"

while True:
    try:
        # Fetch data from the mock API
        response = requests.get(MOCK_URL)
        data = response.json()
        
        # Prepare traffic information
        traffic_info = {
            "location": data.get("location"),
            "congestion_level": data.get("congestion_level"),
            "timestamp": time.time(),
        }
        
        # Send data to Kafka
        producer.send("traffic", value=traffic_info)
        print(f"Sent to 'traffic': {traffic_info}")
        time.sleep(10)  # Fetch data every 10 seconds
    
    except Exception as e:
        print(f"Error fetching or sending traffic data: {e}")

