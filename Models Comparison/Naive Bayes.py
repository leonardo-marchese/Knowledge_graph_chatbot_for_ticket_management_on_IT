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
from sklearn.naive_bayes import MultinomialNB
text_clf = Pipeline([('vect', CountVectorizer()),
           ('tfidf', TfidfTransformer()), ('clf', MultinomialNB()), ])
text_clf.fit(X_train, y_train)
predicted = text_clf.predict(X_test)
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix


def cal_accuracy(y_test, y_pred):
    print("Confusion Matrix: ",
          confusion_matrix(y_test, y_pred))

    print("Accuracy : ",
          accuracy_score(y_test, y_pred) * 100)

cal_accuracy(y_test, predicted)

