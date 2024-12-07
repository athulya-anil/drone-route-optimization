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

def fetch_air_data():
    # Replace with actual traffic API
    # response = requests.get('https://api.trafficdata.com')

    # return response.json()

    locations = [
        {'id': 'Boston', 'latitude': 42.3601, 'longitude': -71.0589},
        {'id': 'Cambridge', 'latitude': 42.3736, 'longitude': -71.1097},
        {'id': 'Worcester', 'latitude': 42.2626, 'longitude': -71.8023},
        {'id': 'Springfield', 'latitude': 42.1015, 'longitude': -72.5898},
        {'id': 'Holyoke', 'latitude': 42.2043, 'longitude': -72.6162},
        {'id': 'Salem', 'latitude': 42.5195, 'longitude': -70.8967},
        {'id': 'Lowell', 'latitude': 42.6334, 'longitude': -71.3162},
        {'id': 'Newton', 'latitude': 42.3370, 'longitude': -71.2092},
        {'id': 'Northampton', 'latitude': 42.3251, 'longitude': -72.6412},
        {'id': 'Framingham', 'latitude': 42.2793, 'longitude': -71.4162}
    ]
    headers = {
    "Content-Type": "application/json"
    }
    username = "userxyz123"
    password = "091mYxuQCx"

    # response = requests.post("https://run.mocky.io/v3/bddd16d8-7c5f-466e-9e11-75463c263bdb",auth=(username, password), headers=headers)
    location_selection = random.randint(0,9)
    value_selection = random.randint(-3,3)
    # print("in airrrr:",location_selection,len(locations),value_selection,len(values))
    air_response = locations[location_selection]|{"update_air":value_selection}
    print("air_response: ", air_response)

    return air_response
    # return {'id': 'Worcester', 'latitude': 42.2626, 'longitude': -71.8023, 'update_air': -0.14}

def fetch_weather_data():
    # headers = {
    # "Content-Type": "application/json"
    # }
    # username = "userxyz123"
    # password = "091mYxuQCx"

    # response = requests.post("https://run.mocky.io/v3/db8f7b49-3171-46dc-b06d-2ef82122a667",auth=(username, password), headers=headers)
    # selection = random.randint(1,7)
    # weather_response = response.json()['data'][str(selection)]
    locations = [
            {'id': 'Boston', 'latitude': 42.3601, 'longitude': -71.0589},
            {'id': 'Cambridge', 'latitude': 42.3736, 'longitude': -71.1097},
            {'id': 'Worcester', 'latitude': 42.2626, 'longitude': -71.8023},
            {'id': 'Springfield', 'latitude': 42.1015, 'longitude': -72.5898},
            {'id': 'Holyoke', 'latitude': 42.2043, 'longitude': -72.6162},
            {'id': 'Salem', 'latitude': 42.5195, 'longitude': -70.8967},
            {'id': 'Lowell', 'latitude': 42.6334, 'longitude': -71.3162},
            {'id': 'Newton', 'latitude': 42.3370, 'longitude': -71.2092},
            {'id': 'Northampton', 'latitude': 42.3251, 'longitude': -72.6412},
            {'id': 'Framingham', 'latitude': 42.2793, 'longitude': -71.4162}
        ] 
    headers = {
    "Content-Type": "application/json"
    }
    username = "userxyz123"
    password = "091mYxuQCx"

    # response = requests.post("https://run.mocky.io/v3/bddd16d8-7c5f-466e-9e11-75463c263bdb",auth=(username, password), headers=headers)
    location_selection = random.randint(0,9)
    value_selection = random.randint(-3,3)
    # print("in weatherrr:",location_selection,len(locations),value_selection,len(values))
    weather_response = locations[location_selection]|{"update_weather":value_selection}
    print("weather_response: ", weather_response)
    return weather_response
    # return {'id': 'Worcester', 'latitude': 42.2626, 'longitude': -71.8023, 'update_weather': 4.12}

while True:
    air_data = fetch_air_data()
    weather_data = fetch_weather_data()
    producer.send('air_topic', air_data)
    producer.send('weather_topic', weather_data)
    print("Sending air and weather data",air_data,weather_data)
    time.sleep(2)
