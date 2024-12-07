import six
import sys
sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaProducer
import json
import time
import requests
import random
# from logger import get_logger

# logger = get_logger(__name__)

# Kafka Producer configuration
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def fetch_air_data():

    response = requests.get('http://localhost:8001/api/air')
    print("air data: ",response.json())
    return response

def fetch_weather_data():

    response = requests.get('http://localhost:8001/api/weather')
    print("weather data: ",response.json())
    return response

while True:
    air_data = fetch_air_data()
    weather_data = fetch_weather_data()

    producer.send('air_topic', air_data)
    producer.send('weather_topic', weather_data)

    # logger.info("Sent air and weather data to Kafka.")
    time.sleep(2)
