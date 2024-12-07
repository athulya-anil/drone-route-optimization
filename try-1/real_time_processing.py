import six
import sys
sys.modules['kafka.vendor.six.moves'] = six.moves

def update_graph_data(graph, data):
    # print("update_graph_data: ",graph.nodes[data['id'].lower()])
    if graph.nodes[data['id'].lower()]:
        if "update_weather" in data.keys():
            print("updating weatherrr",data)
            graph.nodes[data['id'].lower()]["weather_value"] += data["update_weather"]
        if "update_air" in data:
            print("updating airrr",data)
            graph.nodes[data['id'].lower()]["air_space_value"] += data["update_air"]
        # print(data['id'].lower(),"  updated graphhhh: ",graph.nodes[data['id'].lower()])

