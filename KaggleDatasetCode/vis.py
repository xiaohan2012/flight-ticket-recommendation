import networkx as nx
import matplotlib.pyplot as plt


def load_graph():
    G = nx.Graph()

    with open("similar.txt", "r") as f:
        for line in f:
            splitted = line.split("<SEP>")

            G.add_node(splitted[2])
            G.add_node(splitted[3])

            G.add_edge(splitted[2], splitted[3])

    return G

G = load_graph()

nodes = G.nodes
to_delete = []

for node in nodes:
    if G.degree[node] <= 20: to_delete.append(node)

G.remove_nodes_from(to_delete)

to_delete = []

#for node in nodes:
#    if G.degree[node] == 0: to_delete.append(node)

#print(len(to_delete))
#G.remove_nodes_from(to_delete)

nx.draw_circular(G)
plt.savefig("asd.pdf")

print(G.number_of_nodes())
#nx.nx_agraph.write_dot(G, "graph2.dot")

