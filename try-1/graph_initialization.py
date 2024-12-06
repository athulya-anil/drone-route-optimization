from pyspark.sql import SparkSession
from graphframes import GraphFrame
import json
import requests

# Initialize Spark session
spark = SparkSession.builder \
    .appName("GraphInitialization") \
    .config("spark.jars.packages", "graphframes:graphframes:0.8.2-spark3.0-s_2.12") \
    .getOrCreate()

# Load the JSON map data
def fetch_map_data():
    response = requests.get('https://run.mocky.io/v3/4329eee9-1975-4dc9-a655-d0576c4965a4')
    return response.json()

# Fetch initial graph data from Map API
map_data = fetch_map_data()

# Extract vertices (markers)
vertices = spark.createDataFrame(
    [(str(i), marker["name"], marker["latitude"], marker["longitude"]) 
     for i, marker in enumerate(map_data["markers"])],
    ["id", "name", "latitude", "longitude"]
)

# Extract edges (routes)
edges = spark.createDataFrame(
    [
        (str(i), str(j), route["distance"].replace(" km", ""))
        for i, route in enumerate(map_data["routes"])
        for j, waypoint in enumerate(route["waypoints"])
    ],
    ["src", "dst", "weight"]
)

# Create GraphFrame
graph = GraphFrame(vertices, edges)
print("\n\ngraphhhh:\n\n",graph)
graph.cache()

# Save graph to storage for later use
graph.vertices.write.parquet("vertices.parquet")
graph.edges.write.parquet("edges.parquet")

print("Graph initialized and saved to Parquet!")
