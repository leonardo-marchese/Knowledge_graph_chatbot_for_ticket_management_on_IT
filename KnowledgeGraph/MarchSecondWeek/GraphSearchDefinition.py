import NetworkXGraph as nt
import networkx as nx
import matplotlib.pyplot as plt

G = nt.final_graph()

def plot_graph(graph):
    plt.figure(figsize=(8,8))
    pos = nx.spring_layout(graph, k=0.5)
    nx.draw(graph, with_labels=True, node_color='skyblue', node_size=800, edge_cmap=plt.cm.Blues, pos=pos)
    plt.show()

# print("Do Solicitado: " + str(G.adj['Usuario 108']))
# print("Do Chamado: " + str(G.adj['CM0000280']))
# print("Do PC: " + str(G.adj['PC0005113']))
# print("Do Aprovador: " + str(G.adj['Aprovador 591']))
# print("Do AssetType: " + str(G.degree['Notebook Padrão']))
# print(G.nodes['PC0005113'])



# nx_dfs_tree = nx.bfs_tree(G, source='Usuario 104', depth_limit=1)
# nx_dfs_edges = list(nx.dfs_edges(G, source='Usuario 104', depth_limit=2))
# nx_dfs_predecessors = nx.dfs_predecessors(G,source='Usuario 104',depth_limit=2)
# nx_dfs_successors = nx.dfs_successors(G,source='Usuario 104',depth_limit=1)
#
# plot_graph(nx_dfs_tree)
#
# print("__________________ DFS TREE __________________\n")
# print(G.edges('CM0000290'))
# print(nx_dfs_tree.edges())
# print("\n")
# #
# print("__________________ DFS SUCESSORS __________________\n")
# print(G.edges('CM0000290'))
# print(nx_dfs_successors)
# print("\n")

nx_dfs_tree = nx.bfs_tree(G, source='PC0005113', depth_limit=1)
nx_dfs_edges = list(nx.dfs_edges(G, source='PC0005113', depth_limit=2))
nx_dfs_predecessors = nx.dfs_predecessors(G,source='PC0005113',depth_limit=2)
nx_dfs_successors = nx.dfs_successors(G,source='PC0005113',depth_limit=1)

# print("Edges: " + str(nx_dfs_edges))
# print("Predecessors: " + str(nx_dfs_predecessors))
# print("Successor: " + str(nx_dfs_successors))
# plot_graph()

# nx_dfs_tree.add_nodes_from((i, G.nodes[i]) for i in nx_dfs_tree.nodes)


# nodesAt5 = [x for x,y in P.nodes(data=True) if y['at']==5]
# nodesChamado = [j for j,k in G.nodes(data=True) if k['node_type']=='numero_chamado']
# print(nodesChamado)

# nodesAt5 = []
# node_count = 0
# for (p, d) in G.nodes(data=True):
#     node_count = node_count + 1
#     # print("P: " + str(p) + " Contagem: " + str(node_count))
#     print("P: " + str(p) + " Contagem: " + str(node_count) + " D: " + str(d) + " D (Len): " + str(len(d)))

print(nx_dfs_successors)