import networkx as nx
import heapq
import math
import requests
import six
import sys
sys.modules['kafka.vendor.six.moves'] = six.moves

# from logger import get_logger

# logger = get_logger(__name__)

class AStarGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def load_graph(self):

        response = requests.get('https://run.mocky.io/v3/5d9cdad5-f37d-4ffb-ab5d-5fffe6388631')
        mapdata = response.json()
        for nodes in mapdata["nodes"]:
            self.graph.add_node(nodes['id'].lower(),latitude = nodes['latitude'], longitude = nodes['longitude'],weather = nodes["weather"],air_space = nodes["air_space"],weather_value = nodes["weather_value"],air_space_value = nodes["air_space_value"])
            # self.graph.add_node(nodes['id'].lower(),latitude = nodes['latitude'], longitude = nodes['longitude'])
        for edges in mapdata["edges"]:
            self.graph.add_edge(edges['src'].lower(), edges['dst'].lower(), weight=edges['weight'])
        # logger.info("Graph successfully loaded with nodes and edges.")

    def heuristic(self, node_a, node_b):
        lat_a, lon_a = self.graph.nodes[node_a]['latitude'], self.graph.nodes[node_a]['longitude']
        lat_b, lon_b = self.graph.nodes[node_b]['latitude'], self.graph.nodes[node_b]['longitude']
        return math.sqrt((lat_a - lat_b) ** 2 + (lon_a - lon_b) ** 2)

    def astar_with_weights(self, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {node: float('inf') for node in self.graph.nodes}
        g_score[start] = 0

        f_score = {node: float('inf') for node in self.graph.nodes}
        f_score[start] = self.heuristic(start, goal)

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                # Reconstruct the path and weights
                path = []
                weights = []
                while current in came_from:
                    prev = came_from[current]
                    weights.append(self.graph[prev][current]['weight'])
                    path.append(current)
                    current = prev
                path.append(current)
                return path[::-1], weights[::-1]

            for neighbor in self.graph.neighbors(current):
                # Calculate edge weight including environmental factors
                edge_weight = self.graph[current][neighbor]['weight']
                src_weather_quality = self.graph.nodes[current].get("weather_value", 0)
                src_air_quality = self.graph.nodes[current].get("air_space_value", 0)
                dest_weather_quality = self.graph.nodes[neighbor].get("weather_value", 0)
                dest_air_quality = self.graph.nodes[neighbor].get("air_space_value", 0)

                # Add penalties for weather and air space conditions
                penalty = src_weather_quality + src_air_quality + dest_weather_quality + dest_air_quality
                adjusted_weight = edge_weight + penalty

                tentative_g_score = g_score[current] + adjusted_weight

                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return [], []


    def astar_with_intermediates(self, start, goal):
        
        """
        A* algorithm to find the shortest path via one or two intermediate nodes.
        If no valid path exists, return an artificial direct path with a significantly higher weight.
        """
        def find_path(src, dst):
            """
            Helper function to find the shortest path between two points.
            """
            return self.astar_with_weights(src, dst)

        # Try direct path first
        direct_path, direct_weights = find_path(start, goal)
        if direct_path:
            return direct_path, direct_weights, False  # False indicates no artificial path

        # If direct path is not available, try with one intermediate point
        shortest_path = []
        shortest_weights = []
        shortest_distance = float('inf')

        for intermediate in self.graph.nodes:
            if intermediate == start or intermediate == goal:
                continue
            # Find path via one intermediate point
            path1, weights1 = find_path(start, intermediate)
            path2, weights2 = find_path(intermediate, goal)


            if path1 and path2:
                total_distance = sum(weights1) + sum(weights2)
                if total_distance < shortest_distance:
                    shortest_path = path1[:-1] + path2  # Merge paths
                    shortest_weights = weights1 + weights2
                    shortest_distance = total_distance

        if shortest_path:
            return shortest_path, shortest_weights, False

        # No path found, return an artificial direct path
        artificial_weight = (sum(shortest_weights) if shortest_weights else 50) + 100  # Ensure much higher weight
        artificial_path = [start, goal]
        artificial_weights = [artificial_weight]

        return artificial_path, artificial_weights, True  # True indicates an artificial path
