from pyspark.sql import SparkSession
from graphframes import GraphFrame
import requests

# Initialize Spark session
spark = SparkSession.builder \
    .appName("GraphInitialization") \
    .getOrCreate()

def fetch_map_data():
    response = requests.get('https://api.openstreetmap.org')
    return response.json()

# Fetch initial graph data from Map API
map_data = fetch_map_data()

# Create vertices and edges DataFrames
vertices = spark.createDataFrame([(str(node['id']), node['name']) for node in map_data['nodes']], ["id", "name"])
edges = spark.createDataFrame([(str(edge['src']), str(edge['dst']), float(edge['weight'])) for edge in map_data['edges']], ["src", "dst", "weight"])

# Create GraphFrame
graph = GraphFrame(vertices, edges)
graph.cache()

# Save graph to storage for later use
graph.vertices.write.parquet("vertices.parquet")
graph.edges.write.parquet("edges.parquet")
