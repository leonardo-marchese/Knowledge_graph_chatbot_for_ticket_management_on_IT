import NetworkXGraph as nt
import networkx as nx
import matplotlib.pyplot as plt

G = nt.final_graph()

def plot_graph(graph):
    plt.figure(figsize=(8,8))
    pos = nx.spring_layout(graph, k=0.5)
    nx.draw(graph, with_labels=True, node_color='skyblue', node_size=800, edge_cmap=plt.cm.Blues, pos=pos)
    plt.show()

def return_search(graph,search_object):
    nx_dfs_tree = nx.bfs_tree(graph, source=search_object, depth_limit=1)
    nx_dfs_tree.add_nodes_from((i, G.nodes[i]) for i in nx_dfs_tree.nodes)
    return nx_dfs_tree


returned_graph = return_search(G, 'Computador Padrão')

def return_graph_dict(graph):
    aprovador = []
    chamado = []
    tipoPc = []
    pc = []
    usuario = []
    tecnico = []
    grupo = []
    cargo = []
    node_count = 0
    for (p, d) in graph.nodes(data=True):
        if len(d) > 0:
            if d['node_type'] == 'aprovador':
                aprovador.append(p)
            if d['node_type'] == 'numero_chamado':
                chamado.append(p)
            if d['node_type'] == 'pc':
                pc.append(p)
            if d['node_type'] == 'usuario':
                usuario.append(p)
            if d['node_type'] == 'tecnico_resp':
                tecnico.append(p)
            if d['node_type'] == 'grupo_chamado':
                grupo.append(p)
            if d['node_type'] == 'tipo_cargo':
                cargo.append(p)
            if d['node_type'] == 'tipo_pc':
                tipoPc.append(p)

    graph_dict_response = {'aprovador': aprovador,
                           'chamado': chamado,
                           'pc': pc,
                           'usuario': usuario,
                           'tecnico': tecnico,
                           'grupo': grupo,
                           'cargo': cargo,
                           'tipopc': tipoPc
                           }
    return  graph_dict_response

print(return_graph_dict(returned_graph))
