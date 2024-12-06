from flask import Flask, request, jsonify
from route_calculation import AStarGraph

app = Flask(__name__)
graph = AStarGraph()

from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder='.')  # Set template folder to current directory

@app.route('/')
def home():
    return render_template('ui.html')

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
    print("start and end is hereeee: ",start,end)
    path = graph.astar(start, end)
    
    return jsonify({"path": path})



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)