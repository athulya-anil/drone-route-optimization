from flask import Flask, request, jsonify
from route_calculation import AStarGraph

app = Flask(__name__)
graph = AStarGraph()

@app.route('/update_graph', methods=['POST'])
def update_graph():
    updated_edges = request.json['edges']
    # Logic to update the graph with new edges
    for edge in updated_edges:
        graph.graph.add_edge(edge['src'], edge['dst'], weight=edge['weight'])
    return jsonify({"status": "graph updated"})

@app.route('/get_route', methods=['GET'])
def get_route():
    start = request.args.get('start')
    end = request.args.get('end')
    path = graph.astar(start, end)
    return jsonify({"path": path})

if __name__ == '__main__':
    app.run(debug=True)
