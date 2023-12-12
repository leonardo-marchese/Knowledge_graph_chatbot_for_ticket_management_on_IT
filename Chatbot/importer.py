# NLP
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import json

intents = {"intents": [
        {"tag": "saudacao",
         "patterns": ["Oi", "Ola", "Oi tudo bem:", "Tem alguem ai?",
                      "Pode me ajudar", "Bom dia", "Boa Tarde"],
         "responses": ["Ola, como posso te ajudar ?",
                       "Oi, como podemos te ajudar?"]
        },
        {"tag": "despedida",
         "patterns": ["Tchau", "Ate mais", "abracos", "Obrigado", "Obrigado pela ajuda", "Muito obrgado","Voce me ajudou"],
         "responses": ["Até mais, obrigado pela visita!", "Tenha um otimo dia!"]
        },
        {"tag": "novo computador",
         "patterns": ["Gostaria de solicitar um computador", "queria pedir um laptop", "estou com um funcionario novo e gostaria de solicitar um computador", "solicitar pc", "solicitar computador", "solicitar pc", "solicitar computador", "solicitar laptop", "solicitar desktop", "solicitar tablet"],
         "responses": ["Certo, esse computador seria para voce ou outra pessoa?"]
        },
        {"tag": "solicitacao_individual",
         "patterns": ["seria para mim","solicitar computador para mim", "gostaria de ter um computador", "solicito para mim"],
         "responses": ["Qual seria o proposito dessa solicitacao? (Mudanca de funcao, Computador compartilhado)"]
        },
        {"tag": "solicitacao_paraoutro",
         "patterns": ["para outra pessoa", "solicitar computador para outra pessoa", "seria para outra pessoa", "gostaria de solicitar computador para outra pessoa"],
         "responses": ["Poderia me informar o nome dessa pessoa? Caso ainda nao tenha, favor informar seu nome."]
        },
        {"tag": "nome_solicitadopara",
         "patterns": [
             "Usuario 1, User 1, Usua 1, Use 1, Usuario, User, usuario, user, Usuario 10, Usuario 2, Usuario 20, usuario 1, usuario 10, usuario 2, usuario 20, usuario 3, Usuario 3, usuario 30, Usuario 30, usuario 4, Usuario 4, usuario 40, Usuario 40, usuario 5, Usuario 5, Usuario 50, usuario 50,usuario 6, Usuario 6, Usuario 60, usuario 60, usuario 7, Usuario 7, Usuario 70, usuario 70, usuario 8, Usuario 8, Usuario 80, usuario 80, usuario 9, Usuario 9, Usuario 90, usuario 90"],
         "responses": [
             "Qual seria o proposito dessa solicitacao? (Novo funcionario, Mudanca de funcao)"]
         },
        {"tag": "proposito",
         "patterns": ["Novo funcionario", "Mudanca de funcao"],
         "responses": ["A nova funcao sera de Cargo engenharia, Cargo operacional, Cargo Administrativo ou Cargo Adminstrativo Fixo?"]
        },
        {"tag": "proposito2",
         "patterns": ["Computador Compartilhado"],
         "responses": ["Qual seria o proposito dessa solicitacao? (Novo funcionario, Mudanca de funcao)"]
        },
        {"tag": "funcao",
         "patterns": ["Cargo engenharia", "Cargo operacional", "Cargo Administrativo", "Cargo Adminstrativo Fixo"],
         "responses": ["certo, qual seria o modelo que gostaria de solicitar? (Computador Padrao, Notebook Padrao, Computador de Alto Desempenho,Notebook de alto desempenho,  Notebook Dobravel)"]
         },
        {"tag": "modelo",
         "patterns": ["Computador Padrao", "Notebook Padrao", "Computador de Alto Desempenho","Notebook de alto desempenho",  "Notebook Dobravel"],
         "responses": [
             "certo, vou verificar a disponibilidade no sistema, so um minuto!"]
         }

   ]
}

# Tensorflow
import numpy as np
import tflearn
import tensorflow as tf
import random

words = []
classes = []
documents = []
ignore_words = ['?']
# loop through each sentence in our intents patterns
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # tokenize each word in the sentence
        w = nltk.word_tokenize(pattern)
        # add to our words list
        words.extend(w)
        # add to documents in our corpus
        documents.append((w, intent['tag']))
        # add to our classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# stem and lower each word and remove duplicates
words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

# remove duplicates
classes = sorted(list(set(classes)))

# print (len(documents), "documents")
print (len(classes), "classes", classes)
print (len(words), "Palavras Distintas Originadas ", words)

# create our training data
training = []
output = []
# create an empty array for our output
output_empty = [0] * len(classes)

# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # stem each word
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    # create our bag of words array
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # output is a '0' for each tag and '1' for current tag
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

# shuffle our features and turn into np.array
random.shuffle(training)
training = np.array(training)

# create train and test lists
train_x = list(training[:,0])
train_y = list(training[:,1])
# reset underlying graph data
tf.compat.v1.reset_default_graph()
# Build neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]),
                              activation='softmax')
net = tflearn.regression(net)
# Define model and setup tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
# Start training (apply gradient descent algorithm)
model.fit(train_x, train_y, n_epoch=1000, batch_size=8,
                                        show_metric=True)

model.save('model.tflearn')

import pickle
pickle.dump({'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open("training_data", "wb"))

def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))

p = bow("Gostaria de solicitar um computador para meu funcionario", words)
print (p)
print (classes)

#print prediction
print(np.round(model.predict([p])))