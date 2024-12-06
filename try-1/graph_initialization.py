import networkx as nx
import json

def initialize_graph(file_path):
    with open(file_path) as f:
        data = json.load(f)

    graph = nx.DiGraph()
    for node in data["nodes"]:
        graph.add_node(node["id"], latitude=node["latitude"], longitude=node["longitude"])
    for edge in data["edges"]:
        graph.add_edge(edge["src"], edge["dst"], weight=edge["weight"])

    return graph
