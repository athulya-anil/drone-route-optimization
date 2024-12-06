from flask import Flask, request, jsonify, send_from_directory
from route_calculation import AStarGraph
from real_time_processing import update_graph_data

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
    start = request.args.get('start')
    end = request.args.get('end')
    if not start or not end:
        return jsonify({"error": "Both start and end points are required"}), 400
    path = graph.astar(start, end)
    if not path:
        return jsonify({"error": "No route found"}), 404
    result = [{"id": node, "latitude": graph.graph.nodes[node]['latitude'], "longitude": graph.graph.nodes[node]['longitude']} for node in path]
    return jsonify({"path": result})

@app.route('/update_graph', methods=['POST'])
def update_graph():
    data = request.get_json()
    update_graph_data(graph.graph, data)
    return jsonify({"status": "Graph updated successfully"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
