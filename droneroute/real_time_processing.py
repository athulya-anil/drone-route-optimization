import six
import sys
sys.modules['kafka.vendor.six.moves'] = six.moves

# from logger import get_logger

# logger = get_logger(__name__)

def update_graph_data(graph, data):

    if graph.nodes[data['id'].lower()]:
        if "update_weather" in data.keys():
            # logger.info("Updating weather data")
            graph.nodes[data['id'].lower()]["weather_value"] += data["update_weather"]
        if "update_air" in data:
            # logger.info("Updating air data")
            graph.nodes[data['id'].lower()]["air_space_value"] += data["update_air"]

