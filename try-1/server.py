from flask_socketio import SocketIO
from flask import Flask, request, jsonify, send_from_directory
from route_calculation import AStarGraph
from real_time_processing import update_graph_data
from kafka import KafkaConsumer
import json
import threading
import requests

app = Flask(__name__, static_url_path='', static_folder='.')

# Initialize the graph
graph = AStarGraph()
graph.load_graph()

@app.route('/')
def serve_ui():
    # Serve the UI HTML file
    return send_from_directory('.', 'ui.html')

@app.route('/get_route', methods=['GET'])
def get_route():
    
    start = request.args.get('start', '').lower()
    end = request.args.get('end', '').lower()

    if not start or not end:
        return jsonify({"error": "Start and end points are required"}), 400

    try:
        path, weights, artificial = graph.astar_with_intermediates(start, end)
    except KeyError as e:
        return jsonify({"error": f"Node {str(e)} not found in graph"}), 404

    if not path:
        return jsonify({"error": "No route found"}), 404

    for node in path:
        print("graphhhhhh: ",node,graph.graph.nodes[node])

    nodes_data = [
        {
            "id": node,
            "latitude": graph.graph.nodes[node]["latitude"],
            "longitude": graph.graph.nodes[node]["longitude"],
            # "weather": graph.graph.nodes[node].get("weather"),
            # "air_quality": graph.graph.nodes[node].get("air_quality"),
            "weather": graph.graph.nodes[node]["weather"],
            "air_quality": graph.graph.nodes[node]["air_space"],
        }
        for node in path
    ]

    return jsonify({
        "path": path,
        "weights": weights,
        "artificial": artificial,
        "nodes": nodes_data
    })

@app.route('/update_graph', methods=['POST'])
def update_graph():
    data = request.get_json()
    update_graph_data(graph.graph, data)
    return jsonify({"status": "Graph updated successfully"})

# Kafka Consumer configuration
def kafka_listener():
    consumer = KafkaConsumer(
        'weather_topic',
        'air_topic',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    for message in consumer:
        data = message.value
        payload = {}
    
        if message.topic == 'weather_topic':
            payload = {
                "edges": [{"src": data['id'], "dst": data['id'], "weight": data['update_weather']}],
                "update_weather": data['update_weather']
            }
        elif message.topic == 'air_topic':
            payload = {
                "edges": [{"src": data['id'], "dst": data['id'], "weight": data['update_air']}],
                "update_air": data['update_air']
            }

        # Call the /update_graph endpoint
        try:
            response = requests.post("http://localhost:8000/update_graph", json=payload)
            if response.status_code == 200:
                print(f"Graph updated successfully with data: {data}")
            else:
                print(f"Failed to update graph: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error calling /update_graph: {e}")

# Start the Kafka listener in a separate thread
threading.Thread(target=kafka_listener, daemon=True).start()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
