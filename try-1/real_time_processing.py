def update_graph_data(graph, data):
    for edge in data.get("edges", []):
        if graph.has_edge(edge["src"], edge["dst"]):
            graph[edge["src"]][edge["dst"]]["weight"] = edge["weight"]
