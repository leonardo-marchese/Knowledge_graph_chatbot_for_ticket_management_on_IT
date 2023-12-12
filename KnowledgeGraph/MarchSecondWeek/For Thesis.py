import networkx as nx
from KnowledgeGraph.MarchSecondWeek import NetworkXGraph as nt
from KnowledgeGraph.MarchSecondWeek import GraphSearch as search
from datetime import date

G = nt.final_graph()

numero =  ""
dta_solicitacao = date.today()
status = "New"
grupo_responsavel = "Fila de Aprovacao"
tecnico_responsavel = "Responsavel 1"
proposito = ""
descricao = ""
solicitado_por = input("Favor informar seu nome: ")
solicitado_para = "Usuario 1"
funcao = ""
objetivo = 0

search_user_cargo = search.return_graph_dict(search.return_search(G,'CM0000736'))

# search.plot_graph(search.return_search(G,solicitado_para))

print(search_user_cargo)