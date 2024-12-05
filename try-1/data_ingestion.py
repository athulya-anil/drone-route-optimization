import six
import sys
sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaProducer
import json
import time
import requests
import random

# Kafka Producer configuration
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def fetch_traffic_data():
    # Replace with actual traffic API
    # response = requests.get('https://api.trafficdata.com')

    # return response.json()
    
    headers = {
    "Content-Type": "application/json"
    }
    username = "userxyz123"
    password = "091mYxuQCx"

    response = requests.post("https://run.mocky.io/v3/bddd16d8-7c5f-466e-9e11-75463c263bdb",auth=(username, password), headers=headers)
    selection = random.randint(1,3)
    traffic_response = response.json()['data'][str(selection)]

    return traffic_response

def fetch_weather_data():
    headers = {
    "Content-Type": "application/json"
    }
    username = "userxyz123"
    password = "091mYxuQCx"

    response = requests.post("https://run.mocky.io/v3/db8f7b49-3171-46dc-b06d-2ef82122a667",auth=(username, password), headers=headers)
    selection = random.randint(1,7)
    weather_response = response.json()['data'][str(selection)]

    return weather_response

while True:
    traffic_data = fetch_traffic_data()
    weather_data = fetch_weather_data()
    producer.send('traffic_topic', traffic_data)
    producer.send('weather_topic', weather_data)
    print("Sending traffic and weather data")
    time.sleep(2)
