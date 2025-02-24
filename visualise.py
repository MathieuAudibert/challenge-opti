import json
import networkx as nx
import matplotlib.pyplot as plt

data = open('datasets/3_efrei.json').read()  # À modifier par le fichier souhaité
json_data = json.loads(data)

G2 = nx.DiGraph()

for intersection in json_data['intersections']:
    G2.add_node(intersection['id'], pos=(intersection['lat'], intersection['lng']))

for road in json_data['roads']:
    id1 = road['intersectionId1']
    id2 = road['intersectionId2']
    is_one_way = road['isOneWay']
    length = road['length']

    G2.add_edge(id1, id2, length=length, is_one_way=is_one_way)
    if not is_one_way:
        G2.add_edge(id2, id1, length=length, is_one_way=False)

pos = nx.get_node_attributes(G2, 'pos')
plt.figure(figsize=(10, 8))
nx.draw_networkx_nodes(G2, pos, node_size=700, node_color='lightblue')

for edge in G2.edges(data=True):
    if edge[2]['is_one_way']:
        nx.draw_networkx_edges(G2, pos, edgelist=[(edge[0], edge[1])], edge_color='red', width=2, arrows=True)
    else:
        nx.draw_networkx_edges(G2, pos, edgelist=[(edge[0], edge[1])], edge_color='black', width=2, arrows=False)

nx.draw_networkx_labels(G2, pos, font_size=10, font_weight='bold')
edge_labels = {(edge[0], edge[1]): edge[2]['length'] for edge in G2.edges(data=True)}
nx.draw_networkx_edge_labels(G2, pos, edge_labels=edge_labels, font_color='red')

plt.show()
