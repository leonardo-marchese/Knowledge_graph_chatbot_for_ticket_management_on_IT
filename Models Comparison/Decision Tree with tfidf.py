import pandas as pd
from sklearn.model_selection import train_test_split
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import re

dataset = pd.read_excel('C:\\Users\\marchl4\\OneDrive - Caterpillar\\99 - PESSOAL\\UNICAMP\\Mestrado\\TCC\\Projeto2S2023\\Dataset\\UserInputs.xlsx', 'data2')

dataset['Classe'] = dataset['Classe'].map({
    'alvo' : 0,
    'despedida': 1,
    'modelo': 2,
    'perfil': 3,
    'proposito': 4,
    'saudacao': 5,
    'solicitacao': 6,
    'misc': 7

})

x = dataset["Mensagem"]
y = dataset["Classe"]

words = []
ignore_words = []
for item in x:
    w = nltk.word_tokenize(item)
    words.extend(w)

words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

final_list = []

for item in x:
    bag = []
    tokkenized_item = nltk.word_tokenize(item)
    stemming_item = [stemmer.stem(w.lower()) for w in tokkenized_item]
    for z in words:
        bag.append(1) if z in stemming_item else bag.append(0)
    final_list.append(bag)

dataset['bag_message'] = final_list

x_bayes = dataset['bag_message']


X_train, X_test, y_train, y_test = train_test_split(
    x, y, test_size=0.33, random_state=125
)

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.tree import DecisionTreeClassifier
text_clf_gini = Pipeline([('vect', CountVectorizer()),
           ('tfidf', TfidfTransformer()), ('clf', DecisionTreeClassifier(criterion='gini')), ])
text_clf_gini.fit(X_train, y_train)
predicted_gini = text_clf_gini.predict(X_test)
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix


def cal_accuracy(y_test, y_pred):
    print("Confusion Matrix: ",
          confusion_matrix(y_test, y_pred))

    print("Accuracy : ",
          accuracy_score(y_test, y_pred) * 100)

cal_accuracy(y_test, predicted_gini)

print("---------- Entropy -----------")

text_clf_entropy = Pipeline([('vect', CountVectorizer()),
           ('tfidf', TfidfTransformer()), ('clf', DecisionTreeClassifier(criterion='entropy')), ])
text_clf_entropy.fit(X_train, y_train)
predicted_entropy = text_clf_entropy.predict(X_test)
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix


def cal_accuracy(y_test, y_pred):
    print("Confusion Matrix: ",
          confusion_matrix(y_test, y_pred))

    print("Accuracy : ",
          accuracy_score(y_test, y_pred) * 100)

cal_accuracy(y_test, predicted_entropy)