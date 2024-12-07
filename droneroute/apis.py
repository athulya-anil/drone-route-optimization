from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/api/weather', methods=['GET'])
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
    value_selection = random.randint(-3, 3)

    weather_response = locations[location_selection] | {"update_weather": value_selection}

    return jsonify(weather_response)

@app.route('/api/air', methods=['GET'])
def fetch_air_data():
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
    return jsonify(air_response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)
