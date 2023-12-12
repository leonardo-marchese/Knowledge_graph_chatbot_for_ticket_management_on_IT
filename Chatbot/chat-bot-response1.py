# NLP
import nltk
from nltk.stem.lancaster import LancasterStemmer
from datetime import date
import networkx as nx
from KnowledgeGraph.MarchSecondWeek import NetworkXGraph as nt
from KnowledgeGraph.MarchSecondWeek import GraphSearch as search
import time


stemmer = LancasterStemmer()

# importando bibliotecas
import numpy as np
import tflearn
import tensorflow as tf
import random

# In[2]:

def goto(linenum):
    global line
    line = linenum

# carregando a estrutura da rede
import pickle
data = pickle.load(open("training_data", "rb"))
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

# carregando as intencoes
import json
with open('intents.json') as json_data:
    intents = json.load(json_data)

# In[3]:

# Construindo a rede
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

# Deinindo configuracoes do Tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')


def clean_up_sentence(sentence):
    # tokenizando frases
    sentence_words = nltk.word_tokenize(sentence)
    # stem
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words


def bow(sentence, words, show_details=False):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)

    return (np.array(bag))


# load our saved model
model.load('./model.tflearn')

context = {}

ERROR_THRESHOLD = 0.25


def classify(sentence):
    results = model.predict([bow(sentence, words)])[0]
    results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    return return_list


def response(sentence, userID='123', show_details=False):
    results = classify(sentence)
    if results:
        while results:
            for i in intents['intents']:
                if i['tag'] == results[0][0]:
                    if 'context_set' in i:
                        if show_details: print('context:', i['context_set'])
                        context[userID] = i['context_set']

                    if not 'context_filter' in i or (
                            userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                        if show_details: print('tag:', i['tag'])
                        # sorteia uma resposta da intenção
                        return print("ChatBot:", random.choice(i['responses']))

            # results.pop(0)


# funcao para receber frases e dar respostas com detalhes
def mensagem(frase):
    response(frase, show_details=False)


# Pesquisa no grafo e chat
G = nt.final_graph()

numero =  ""
dta_solicitacao = date.today()
status = "New"
grupo_responsavel = "Fila de Aprovacao"
tecnico_responsavel = "Responsavel 1"
proposito = ""
descricao = ""
solicitado_por = input("Favor informar seu nome: ")
solicitado_para = ""
funcao = ""
objetivo = 0


# search_user_cargo = search.return_graph_dict(search.return_search(G,solicitado_para))

while True:

    msg = input("User: ")
    classfied = classify(msg)
    mensagem(msg)
    if classfied[0][0] == "despedida":
        break
    if classfied[0][0] == "proposito":
        proposito = msg
    if classfied[0][0] == "funcao":
        funcao = msg
    if classfied[0][0] == "solicitacao_individual":
            objetivo = 1
            solicitado_para = solicitado_por
    if classfied[0][0] == "solicitacao_paraoutro":
            objetivo = 2
            solicitado_para = msg

    if classfied[0][0] == "nome_solicitadopara":
        solicitado_para = msg
    if classfied[0][0] == "modelo":
        descricao = msg

        if objetivo == 1:

            search_modelo_cargo = search.return_graph_dict(search.return_search(G, descricao.lower()))
            search_user_info = search.return_graph_dict(search.return_search(G, solicitado_para))
            user_open_tickets = search.get_open_tickets(search_user_info)

            if funcao.lower() == str.lower(search_modelo_cargo['cargo'][0]):

                if len(search_user_info['pc']) > 0:
                    time.sleep(2)
                    print("Chatbot: Me desculpe, mas no sistema consta que você ja utiliza os seguintes computadores: " + str(search_user_info['pc']))

                    uso = input("Voce continuará usando algum? S/N R: ")
                    if uso == "S":
                        print("Chatbot: Nesse caso nao poderei dar continuidade no chamado! Favor contatar o suporte local.")

                    if uso == "N":
                        print("Chatbot: Informar Node do computador + virgula + Nome do novo Responsavel (Caso tenha mais de um computador, utilizar ponto e virgula na mesma linha para cada computador)")
                        mudanca_pc = input("User: ")
                        time.sleep(2)
                        if len(search.get_open_tickets(search_user_info)) > 0:
                            print("Chatbot: Obrigado por aguardar, ja fiz a alteracao no sistema.")
                        else:
                            print("Chatbot: Obrigado por aguardar, ja fiz a alteracao no sistema.Posso ajudar com mais alguma coisa?")

                    if len(search.get_open_tickets(search_user_info)) > 0:
                        time.sleep(2)
                        print("Chatbot: Me desculpe a insistencia, porem no sistema consta que você existem solicitacoes de computadores pendentes em seu nome, solicitacao: " + str(search.get_open_tickets(search_user_info)))
                        resposta_chamados = input("Chatbot: Voce gostaria de solicitar um novo mesmo? S/N: ")

                        if resposta_chamados == "S" or resposta_chamados == "s":
                            print("Chatbot: Entao estou abrindo esse chamado para você, so um minuto.")
                            time.sleep(2)
                            print("Chatbot: Posso te ajudar com mais alguma coisa?")
                        elif resposta_chamados == "N" or resposta_chamados == "n":
                            print("Chatbot: Posso te ajudar com mais alguma coisa?")
                    else:
                        print("Chatbot: Posso te ajudar com mais alguma coisa?")

            else:
                time.sleep(2)
                print("Chatbot: Me desculpe, esse perfil nao tem autorizacao para solicitar esse modelo! Favor contatar o suporte local.")
                time.sleep(2)
                print("Chatbot: Posso te ajudar com mais alguma coisa?")

        if objetivo == 2:
            search_modelo_cargo = search.return_graph_dict(search.return_search(G, descricao.lower()))

            if solicitado_por == solicitado_para:
                search_user_info = search.return_graph_dict(search.return_search(G, solicitado_para))
            else:
                try:
                    search_new_user = search.return_graph_dict(search.return_search(G, solicitado_para))
                except:
                    G.add_node(solicitado_para)
                    G.add_edge(solicitado_para,funcao)
                search_user_info = search.return_graph_dict(search.return_search(G, solicitado_para))




            if funcao.lower() == str.lower(search_modelo_cargo['cargo'][0]):

                    search_requestor_info = search.return_graph_dict(search.return_search(G, solicitado_por))

                    if len(search_requestor_info['pc']) > 0:
                        time.sleep(2)
                        print(
                            "Chatbot: Me desculpe, mas no sistema consta que a pessoa ja utiliza os seguintes computadores: " + str(
                                search_requestor_info['pc']))

                        uso = input("Voce continuará usando algum? S/N R: ")
                        if uso == "S":
                            print(
                                "Chatbot: Nesse caso nao poderei dar continuidade no chamado! Favor contatar o suporte local.")

                        if uso == "N":
                            print(
                                "Chatbot: Informar Node do computador + virgula + Nome do novo Responsavel (Caso tenha mais de um computador, utilizar ponto e virgula na mesma linha para cada computador)")
                            mudanca_pc = input("User: ")
                            time.sleep(2)
                            if len(search.get_open_tickets(search_requestor_info)) > 0:
                                print("Chatbot: Obrigado por aguardar, ja fiz a alteracao no sistema.")
                            else:
                                print(
                                    "Chatbot: Obrigado por aguardar, ja fiz a alteracao no sistema.Posso ajudar com mais alguma coisa?")

                    if len(search.get_open_tickets(search_requestor_info)) > 0:
                        time.sleep(2)
                        print("Chatbot: Me desculpe a insistencia, porem no sistema consta que você existem solicitacoes de computadores pendentes em seu nome, solicitacao: " + str(search.get_open_tickets(search_requestor_info)))
                        resposta_chamados = input("Chatbot: Voc6e gostaria de solicitar um novo mesmo? S/N: ")

                        if resposta_chamados == "S" or resposta_chamados == "s":
                            print("Chatbot: Entao estou abrindo esse chamado para você, so um minuto.")
                            time.sleep(2)
                            print("Chatbot: Posso te ajudar com mais alguma coisa?")
                        elif resposta_chamados == "N" or resposta_chamados == "n":
                            print("Chatbot: Posso te ajudar com mais alguma coisa?")
                    else:
                        print("Chatbot: Posso te ajudar com mais alguma coisa?")

            else:
                time.sleep(2)
                print("Chatbot: Me desculpe, esse perfil nao tem autorizacao para solicitar esse modelo! Favor contatar o suporte local.")
                time.sleep(2)
                print("Chatbot: Posso te ajudar com mais alguma coisa?")





# Transformar resultado do Grafo em Dicionario e utilizar aqui






