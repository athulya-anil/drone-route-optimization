import networkx as nx
import heapq
import math
import requests

class AStarGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def load_graph(self):
        self.graph.add_node("A", latitude=0, longitude=0)
        self.graph.add_node("B", latitude=1, longitude=1)
        self.graph.add_edge("A", "B", weight=1)
    # def load_graph(self):
    #     response = requests.get('https://run.mocky.io/v3/4329eee9-1975-4dc9-a655-d0576c4965a4')
    #     return response.json()

    def heuristic(self, node_a, node_b):
        lat_a, lon_a = self.graph.nodes[node_a]['latitude'], self.graph.nodes[node_a]['longitude']
        lat_b, lon_b = self.graph.nodes[node_b]['latitude'], self.graph.nodes[node_b]['longitude']
        return math.sqrt((lat_a - lat_b) ** 2 + (lon_a - lon_b) ** 2)

    def astar(self, start, goal):
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
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(current)
                return path[::-1]

            for neighbor in self.graph.neighbors(current):
                tentative_g_score = g_score[current] + self.graph[current][neighbor]['weight']
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []
