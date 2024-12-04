from kafka import KafkaProducer
import json
import time
import requests

# Kafka Producer configuration
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def fetch_traffic_data():
    # Replace with actual traffic API
    response = requests.get('https://api.trafficdata.com')
    return response.json()

def fetch_weather_data():
    # Replace with actual weather API
    # response = requests.get('https://api.weatherdata.com')
    response = requests.get('api.meteomatics.com/2024-12-04T00:00:00Z--2024-12-07T00:00:00Z:PT1H/t_2m:C/52.520551,13.461804/json')
    return response.json()

while True:
    traffic_data = fetch_traffic_data()
    weather_data = fetch_weather_data()
    producer.send('traffic_topic', traffic_data)
    producer.send('weather_topic', weather_data)
    time.sleep(2)
