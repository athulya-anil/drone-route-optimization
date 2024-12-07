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

    location_selection = random.randint(0, len(locations) - 1)
    value_selection = random.randint(-3,3)

    # logger.info("Fetching air data...")

    air_response = locations[location_selection]|{"update_air":value_selection}
    return air_response

def fetch_weather_data():

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

    location_selection = random.randint(0, len(locations) - 1)
    value_selection = random.randint(-3,3)

    # logger.info("Fetching weather data...")

    weather_response = locations[location_selection]|{"update_weather":value_selection}
    return weather_response

while True:
    air_data = fetch_air_data()
    weather_data = fetch_weather_data()

    producer.send('air_topic', air_data)
    producer.send('weather_topic', weather_data)

    # logger.info("Sent air and weather data to Kafka.")
    time.sleep(2)
