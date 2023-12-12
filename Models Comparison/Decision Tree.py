import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import re

dataset = pd.read_excel('C:\\Users\\marchl4\\OneDrive - Caterpillar\\99 - PESSOAL\\UNICAMP\\Mestrado\\TCC\\Projeto2S2023\\Dataset\\UserInputs.xlsx', 'data')

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

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

from sklearn.feature_extraction.text import TfidfVectorizer

vectorization = TfidfVectorizer()
xv_train = vectorization.fit_transform(x_train)
xv_test = vectorization.transform(x_test)


def prediction(X_test, model_object):
    # Predicton on test with giniIndex
    y_pred = model_object.predict(xv_test)
    print("Predicted values:")
    print(y_pred)
    return y_pred


def cal_accuracy(y_test, y_pred):
    print("Confusion Matrix: ",
          confusion_matrix(y_test, y_pred))

    print("Accuracy : ",
          accuracy_score(y_test, y_pred) * 100)

print("----------- Gini -----------")
# Decision tree with gini
model_gini = DecisionTreeClassifier(criterion="gini",
                                    random_state=123, max_depth=10, min_samples_leaf=6)

# Performing training
model_gini.fit(xv_train, y_train)

# Prediction using gini
y_pred_gini = prediction(xv_test, model_gini)
cal_accuracy(y_test, y_pred_gini)

print("----------- Entropy -----------")

# Decision tree with entropy
model_entropy = DecisionTreeClassifier(
    criterion="entropy", random_state=123,
    max_depth=10, min_samples_leaf=6)

# Performing training
model_entropy.fit(xv_train, y_train)

# Prediction using entropy
y_pred_entropy = prediction(xv_test, model_entropy)
cal_accuracy(y_test, y_pred_entropy)

