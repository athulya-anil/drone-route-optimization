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
MOCK_URL = "https://run.mocky.io/v3/85043c2e-6d85-4ef1-8b28-80381ee7118b"

while True:
    try:
        # Fetch data from the mock API
        response = requests.get(MOCK_URL)
        data = response.json()
        
        # Prepare weather information
        weather_info = {
            "city": data.get("city"),
            "temperature": data.get("temperature"),
            "conditions": data.get("conditions"),
            "timestamp": time.time(),
        }
        
        # Send data to Kafka
        producer.send("weather", value=weather_info)
        print(f"Sent to 'weather': {weather_info}")
        time.sleep(10)  # Fetch data every 10 seconds
    
    except Exception as e:
        print(f"Error fetching or sending weather data: {e}")

