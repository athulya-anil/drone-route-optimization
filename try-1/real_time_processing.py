import six
import sys
sys.modules['kafka.vendor.six.moves'] = six.moves

def update_graph_data(graph, data):
    for edge in data.get("edges", []):
        # Update edge weights
        if graph.has_edge(edge["src"], edge["dst"]):
            graph[edge["src"]][edge["dst"]]["weight"] += edge["weight"]

        # Update node attributes (weather and air quality)
        src_node = edge["src"]
        if src_node in graph.nodes:
            if "update_weather" in data:
                graph.nodes[src_node]["weather_value"] += data["update_weather"]
            if "update_air" in data:
                graph.nodes[src_node]["air_space_value"] += data["update_air"]

