from KnowledgeGraph.MarchSecondWeek import NetworkXGraph as nt
import networkx as nx
import matplotlib.pyplot as plt

G = nt.final_graph()

def plot_graph(graph):
    plt.figure(figsize=(8,8))
    pos = nx.spring_layout(graph, k=0.5)
    nx.draw(graph, with_labels=False, node_color='skyblue', node_size=800, edge_cmap=plt.cm.Blues, pos=pos)
    plt.show()

def return_search(graph,search_object):
    nx_dfs_tree = nx.bfs_tree(graph, source=search_object,
                                            depth_limit=1)
    nx_dfs_tree.add_nodes_from((i, G.nodes[i])
                               for i in nx_dfs_tree.nodes)
    return  nx_dfs_tree



def return_graph_dict(searched_graph):
    aprovador = []
    chamado = []
    chamado_status = []
    chamado_aberto = []
    chamado_tipoPC = []
    tipoPc = []
    periferico = []
    pc = []
    usuario = []
    tecnico = []
    grupo = []
    cargo = []
    for (p, d) in searched_graph.nodes(data=True):
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
            if d['node_type'] == 'periferico':
                periferico.append(p)

    for ticket in chamado:
        ticket_response = return_search(G,ticket)
        # print(ticket_response.nodes(data=True))
        for (e, f) in ticket_response.nodes(data=True):
            if len(f) > 0:
                if f['node_type'] == 'numero_chamado':
                    chamado_status.append(f['Status'])
                    chamado_aberto.append(f['Data Solicitação'])

    graph_dict_response = {'aprovador': aprovador,
                           'chamado': chamado,
                           'chamado_status': chamado_status,
                           'chamado_aberto': chamado_aberto,
                           'pc': pc,
                           'usuario': usuario,
                           'tecnico': tecnico,
                           'grupo': grupo,
                           'cargo': cargo,
                           'modelo': tipoPc,
                           'periferico': periferico
                           }
    return  graph_dict_response

def get_open_tickets(graph_dict):
    open_tickets = []
    count = -1
    for i in graph_dict['chamado']:
        count = count + 1
        if graph_dict['chamado_status'][count] in ['Open', 'Pending', 'Work in Progress', 'On Hold']:
            tipoPc_chamado = return_search(G, graph_dict['chamado'][count])
            for (g, h) in tipoPc_chamado.nodes(data=True):
                if len(h) > 0:
                    if h['node_type'] == 'tipo_pc':
                        if g in ['computador de alto desempenho', 'computador nao registrado', 'computador padrao',
                                 'notebook de alto desempenho', 'notebook dobravel', 'notebook padrao',
                                 'notebook robusto', 'tablet']:

                            open_tickets.append(graph_dict['chamado'][count])
    return open_tickets


def return_edge_dict(searched_graph):

    edge_pc_tipoNode = []
    edge_pc_tipoCargo = []
    edge_tipoNode_tipoCargo = []
    edge_num_descricao = []
    edge_solpara_num = []
    edge_aprovador_num = []
    edge_num_proposito = []
    edge_num_grupo = []
    edge_num_tecnico = []
    edge_primOwner_pc = []
    edge_userPeriferico_periferico = []
    edge_perfil_periferico = []
    edge_userNode_userType = []

    g_edges = list(searched_graph.edges(data=True))
    # for i in g_edges[0][2]['edge_type']:
    for i in g_edges:
        if i[2]['edge_type'] == 'pc_tipoNode':
            edge_pc_tipoNode.append(list([i[0], i[1]]))
        if i[2]['edge_type'] == 'pc_tipoCargo':
            edge_pc_tipoCargo.append(list([i[0], i[1]]))
        if i[2]['edge_type'] == 'tipoNode_tipoCargo':
            edge_tipoNode_tipoCargo.append(list([i[0], i[1]]))
        if i[2]['edge_type'] == 'num_descricao':
            edge_num_descricao.append(list([i[0], i[1]]))
        if i[2]['edge_type'] == 'solpara_num':
            edge_solpara_num.append(list([i[0], i[1]]))
        if i[2]['edge_type'] == 'aprovador_num':
            edge_aprovador_num.append(list([i[0], i[1]]))
        if i[2]['edge_type'] == 'num_proposito':
            edge_num_proposito.append(list([i[0], i[1]]))
        if i[2]['edge_type'] == 'num_grupo':
            edge_num_grupo.append(list([i[0], i[1]]))
        if i[2]['edge_type'] == 'num_tecnico':
            edge_num_tecnico.append(list([i[0], i[1]]))
        if i[2]['edge_type'] == 'primOwner_pc':
            edge_primOwner_pc.append(list([i[0], i[1]]))
        if i[2]['edge_type'] == 'userPeriferico_periferico':
            edge_userPeriferico_periferico.append(list([i[0], i[1]]))
        if i[2]['edge_type'] == 'perfil_periferico':
            edge_perfil_periferico.append(list([i[0], i[1]]))
        if i[2]['edge_type'] == 'userNode_userType':
            edge_userNode_userType.append(list([i[0], i[1]]))

    graph_dict_edges = { 'pc_tipoNode' : edge_pc_tipoNode,
                         'pc_tipoCargo' : edge_pc_tipoCargo,
                         'tipoNode_tipoCargo' : edge_tipoNode_tipoCargo,
                         'num_descricao' : edge_num_descricao,
                         'solpara_num' : edge_solpara_num,
                         'aprovador_num' : edge_aprovador_num,
                         'num_proposito' : edge_num_proposito,
                         'num_grupo' : edge_num_grupo,
                         'num_tecnico' : edge_num_tecnico,
                         'primOwner_pc' : edge_primOwner_pc,
                         'userPeriferico_periferico': edge_userPeriferico_periferico,
                         'perfil_periferico': edge_perfil_periferico,
                         'userNode_userType': edge_userNode_userType

                         }
    return graph_dict_edges




