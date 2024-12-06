import networkx as nx
import json
import six
import sys
sys.modules['kafka.vendor.six.moves'] = six.moves

def initialize_graph(file_path):
    with open(file_path) as f:
        data = json.load(f)

    graph = nx.DiGraph()
    for node in data["nodes"]:
        graph.add_node(node['id'].lower(),latitude = node['latitude'], longitude = node['longitude'],weather = node["weather"],air_space = node["air_space"],weather_value = node["weather_value"],air_space_value = node["air_space_value"])
    for edge in data["edges"]:
        graph.add_edge(edge["src"], edge["dst"], weight=edge["weight"])

    return graph
