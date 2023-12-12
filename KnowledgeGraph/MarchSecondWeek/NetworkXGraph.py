import networkx as nx
import pandas as pd




G = nx.Graph()

estrutura_grafo_file = 'C:\\Users\\marchl4\OneDrive - Caterpillar\\99 - PESSOAL\\UNICAMP\Mestrado\\TCC\\Projeto1S2022\\KnowledgeGraph\\Dataset\\March Second Week\\estrutura_grafo.xlsx'



#---------------------- Para Chamado ---------------------------

pd_chamado_node = pd.read_excel(estrutura_grafo_file, sheet_name='Chamado')
numero_node = list(pd_chamado_node['Numero'])
descricao_node = list(pd_chamado_node['Descrição'])
solicitadoPara_node = list(pd_chamado_node['Solicitado Para'])
aprovador_node = list(pd_chamado_node['Aprovador'])
proposito_node = list(pd_chamado_node['Proposito'])
grupo_node = list(pd_chamado_node['Grupo Responsavel'])
tecnico_node = list(pd_chamado_node['Tecnico Responsavel'])

numDescricao_relationship = [(numero_node[i], descricao_node[i]) for i in range(0, len(numero_node))]
solicitadoNum_relationship = [(solicitadoPara_node[i], numero_node[i]) for i in range(0, len(solicitadoPara_node))]
aprovadorNum_relationship = [(aprovador_node[i], numero_node[i]) for i in range(0, len(aprovador_node))]
propnum_relationship = [(numero_node[i], proposito_node[i]) for i in range(0, len(numero_node))]
grupnum_relationship = [(numero_node[i], grupo_node[i]) for i in range(0, len(numero_node))]
tecpnum_relationship = [(numero_node[i], tecnico_node[i]) for i in range(0, len(numero_node))]

G.add_nodes_from(numero_node,node_type='numero_chamado')
G.add_nodes_from(descricao_node,node_type='tipo_pc')
G.add_nodes_from(solicitadoPara_node,node_type='usuario')
G.add_nodes_from(aprovador_node,node_type='aprovador')
G.add_nodes_from(grupo_node,node_type='gr upo_chamado')
G.add_nodes_from(tecnico_node,node_type='tecnico_resp')

G.add_edges_from(numDescricao_relationship,
                 edge_type='num_descricao')
G.add_edges_from(solicitadoNum_relationship,
                 edge_type='solpara_num')
G.add_edges_from(aprovadorNum_relationship,
                 edge_type='aprovador_num')
G.add_edges_from(propnum_relationship,
                 edge_type='num_proposito')
G.add_edges_from(grupnum_relationship,
                 edge_type='num_grupo')
G.add_edges_from(tecpnum_relationship,
                 edge_type='num_tecnico')

#---------------------- Para Usuario Computador --------------------------

pd_primaryOwner_node = pd.read_excel(estrutura_grafo_file, sheet_name='PrimaryOwner_rels')

po_pc_node = list(pd_primaryOwner_node['PC'])
po_user_node = list(pd_primaryOwner_node['User'])

po_pcUser_relationship = [(po_user_node[i], po_pc_node[i]) for i in range(0, len(po_user_node))]

G.add_nodes_from(po_pc_node,node_type='pc')
G.add_nodes_from(po_user_node,node_type='usuario')
G.add_edges_from(po_pcUser_relationship, edge_type='primOwner_pc')

#
# print("Do PC: " + str(G.adj['PC0002959']))
# print("Do Usuario: " + str(G.adj['Usuario 1']))


#---------------------- Para Computador --------------------------

pd_pc_node = pd.read_excel(estrutura_grafo_file, sheet_name='Computador')

pc_node = list(pd_pc_node['ID'])
tipo_node = list(pd_pc_node['Tipo'])
tipoCargo_node = list(pd_pc_node['Perfil Computador'])

pctipo_relationship = [(pc_node[i], tipo_node[i]) for i in range(0, len(pc_node))]
pcCargo_relationship = [(pc_node[i], tipoCargo_node[i]) for i in range(0, len(tipoCargo_node))]
tipoCargo_relationship = [(tipo_node[i], tipoCargo_node[i]) for i in range(0, len(tipo_node))]

G.add_nodes_from(pc_node,node_type='pc')
G.add_nodes_from(tipo_node,node_type='tipo_pc')
G.add_nodes_from(tipoCargo_node,node_type='tipo_cargo')
G.add_edges_from(pctipo_relationship, edge_type='pc_tipoNode')
G.add_edges_from(pcCargo_relationship, edge_type='pc_tipoCargo')
G.add_edges_from(tipoCargo_relationship, edge_type='tipoNode_tipoCargo')


#---------------------- Para Usuario --------------------------

pd_user_node = pd.read_excel(estrutura_grafo_file, sheet_name='Usuario')

user_node = list(pd_user_node['Usuario'])
userType_node = list(pd_user_node['Perfil Cargo'])

G.add_nodes_from(user_node,node_type='usuario')
G.add_nodes_from(userType_node,node_type='tipo_cargo')

userType_relationship = [(user_node[i], userType_node[i]) for i in range(0, len(user_node))]

G.add_edges_from(userType_relationship,edge_type='userNode_userType')

#---------------------- Para Periferico --------------------------

pd_user_node = pd.read_excel(estrutura_grafo_file, sheet_name='Periferico')

user_per_node = list(pd_user_node['Usuario'])
periferico_node = list(pd_user_node['Periferico'])
perfil_node = list(pd_user_node['Perfil Cargo'])


# G.add_nodes_from(user_node,node_type='usuario')
G.add_nodes_from(periferico_node,node_type='periferico')

userper_relationship = [(user_per_node[i], periferico_node[i]) for i in range(0, len(user_per_node))]
profile_relationship = [(perfil_node[i], periferico_node[i]) for i in range(0, len(perfil_node))]

G.add_edges_from(userper_relationship, edge_type='userPeriferico_periferico')
G.add_edges_from(profile_relationship, edge_type='perfil_periferico')

#---------------------- Para Atributos --------------------------

pd_chamado_attrs = pd_chamado_node[['Numero', 'Data Solicitação', 'Status']].drop_duplicates()
node_chamado_attr = pd_chamado_attrs.set_index('Numero').to_dict('index')
nx.set_node_attributes(G, node_chamado_attr)

#Removidos valores duplicados manualmente (Normalmente foram os itens uma vez instalado e depois perdidos / aposentados)
pd_pc_attrs = pd_pc_node[['ID', 'Status', 'Ultimo Acesso', 'Prazo de Garantia']].drop_duplicates()
node_pc_attr = pd_pc_attrs.set_index('ID').to_dict('index')
nx.set_node_attributes(G, node_pc_attr)


def final_graph():

    return G



