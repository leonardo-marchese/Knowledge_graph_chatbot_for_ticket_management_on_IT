from pyvis.network import Network
import pandas as pd

net = Network(directed=True)

estrutura_grafo_file = '/KnowledgeGraph/Dataset/MarchSecondWeek/estrutura_grafo.xlsx'

pd_ticket_node = pd.read_excel(estrutura_grafo_file, sheet_name='Numero')

ticket_node_label = list(pd_ticket_node['label_numero'])
ticket_node_id = list(pd_ticket_node['id_numero'])

net.add_nodes(ticket_node_id, label=ticket_node_label)


pd_assetType_node = pd.read_excel(estrutura_grafo_file, sheet_name='Descrição')

assetType_node_label = list(pd_assetType_node['label_descricao'])
assetType_node_id = list(pd_assetType_node['id_descricao'])

net.add_nodes(assetType_node_id, label=assetType_node_label)

ticket_assetType_rels = pd.read_excel(estrutura_grafo_file, sheet_name='rels_Numero_Descricao')

from_numero = list(map(int, list(ticket_assetType_rels['from_numero'].dropna())))
to_ticket = list(map(int, list(ticket_assetType_rels['to_descricao'].dropna())))
numTicket_relationship = [(from_numero[i], to_ticket[i]) for i in range(0, len(from_numero))]

pd_solicitado_node = pd.read_excel(estrutura_grafo_file, sheet_name='solicitado')

solicitado_node_label = list(pd_solicitado_node['label_solicitado'])
solicitado_node_id = list(pd_solicitado_node['id_solicitado'])

net.add_nodes(solicitado_node_id, label=solicitado_node_label)

ticket_Solicitado_rels = pd.read_excel(estrutura_grafo_file, sheet_name='rels_Numero_Solicitado')

from_solicitado = list(map(int, list(ticket_Solicitado_rels['from_solicitado'].dropna())))
to_Numero = list(map(int, list(ticket_Solicitado_rels['to_Numero'].dropna())))
SolTicket_relationship = [(from_solicitado[i], to_Numero[i]) for i in range(0, len(from_solicitado))]

pd_Approver_node = pd.read_excel(estrutura_grafo_file, sheet_name='Aprovador')

Approver_node_label = list(pd_Approver_node['label_aprovador'])
Approver_node_id = list(pd_Approver_node['id_aprovador'])

net.add_nodes(Approver_node_id, label=Approver_node_label)

ticket_Aprovador_rels = pd.read_excel(estrutura_grafo_file, sheet_name='rels_Numero_Aprovador')

from_aprovador = list(map(int, list(ticket_Aprovador_rels['from_aprovador'].dropna())))
to_Num = list(map(int, list(ticket_Aprovador_rels['to_numero'].dropna())))
AprTicket_relationship = [(from_aprovador[i], to_Num[i]) for i in range(0, len(from_aprovador))]

pd_purpose_node = pd.read_excel(estrutura_grafo_file, sheet_name='Proposito')

purpose_node_label = list(pd_purpose_node['label_proposito'])
purpose_node_id = list(pd_purpose_node['id_proposito'])

net.add_nodes(purpose_node_id, label=purpose_node_label)

ticket_purpose_rels = pd.read_excel(estrutura_grafo_file, sheet_name='rels_Numero_Proposito')

from_num1 = list(map(int, list(ticket_purpose_rels['from_numero'].dropna())))
to_purpose = list(map(int, list(ticket_purpose_rels['to_proposito'].dropna())))
numPurpose_relationship = [(from_num1[i], to_purpose[i]) for i in range(0, len(from_aprovador))]

#----------------------------------Computer---------------------------------------

pd_pc_node = pd.read_excel(estrutura_grafo_file, sheet_name='PC')

pc_node_label = list(pd_pc_node['pc_label'])
pc_node_id = list(pd_pc_node['pc_id'])

net.add_nodes(pc_node_id, label=pc_node_label)

pc_descricao_rels = pd.read_excel(estrutura_grafo_file, sheet_name='pc_descricao_rels')

from_pc = list(map(int, list(pc_descricao_rels['from_pc'].dropna())))
to_descricao = list(map(int, list(pc_descricao_rels['to_descricao'].dropna())))
pcDescricao_relationship = [(from_pc[i], to_descricao[i]) for i in range(0, len(from_pc))]

pd_owner_node = pd.read_excel(estrutura_grafo_file, sheet_name='Responsavel')

owner_node_label = list(pd_owner_node['responsavel_label'])
owner_node_id = list(pd_owner_node['responsavel_id'])

net.add_nodes(owner_node_id, label=owner_node_label)

pd_PrimUser_node = pd.read_excel(estrutura_grafo_file, sheet_name='PrimaryUser')

PrimUser_node_label = list(pd_PrimUser_node['usuariopri_label'])
PrimUser_node_id = list(pd_PrimUser_node['usuariopri_id'])

net.add_nodes(PrimUser_node_id, label=PrimUser_node_label)

primOwner_descricao_rels = pd.read_excel(estrutura_grafo_file, sheet_name='PrimaryOwner_rels')

from_User = list(map(int, list(primOwner_descricao_rels['usuario_from'].dropna())))
to_pc = list(map(int, list(primOwner_descricao_rels['pc_to'].dropna())))
Userpc_relationship = [(from_User[i], to_pc[i]) for i in range(0, len(from_User))]

net.repulsion(node_distance=1000, spring_length=100)
net.show_buttons(filter_=["physics"])

net.add_edges(numTicket_relationship)
net.add_edges(SolTicket_relationship)
net.add_edges(AprTicket_relationship)
net.add_edges(numPurpose_relationship)
net.add_edges(pcDescricao_relationship)
net.add_edges(Userpc_relationship)

net.show('2_user_test.html')


