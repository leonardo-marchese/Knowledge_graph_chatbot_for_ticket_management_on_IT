import numpy as np
import tensorflow as tf
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import pandas as pd

# Suponha que você tenha um DataFrame chamado 'df' com colunas 'texto' e 'classe'
# Substitua isso pelos seus dados reais
df = pd.read_excel('C:\\Users\\marchl4\\OneDrive - Caterpillar\\99 - PESSOAL\\UNICAMP\\Mestrado\\TCC\\Projeto2S2023\\Dataset\\UserInputs.xlsx', 'data')

df['Classe'] = df['Classe'].map({
    'alvo' : 0,
    'despedida': 1,
    'modelo': 2,
    'perfil': 3,
    'proposito': 4,
    'saudacao': 5,
    'solicitacao': 6,
    'misc': 7

})

texts = df["Mensagem"]
labels = df["Classe"]

# Pré-processamento: Divida os dados em treino e teste
texts_train, texts_test, labels_train, labels_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

# Pré-processamento: Aplicar TF-IDF nos textos
vectorizer = TfidfVectorizer(max_features=5000)  # Ajuste o número máximo de features conforme necessário
tfidf_train = vectorizer.fit_transform(texts_train).toarray()
tfidf_test = vectorizer.transform(texts_test).toarray()

# Construa o modelo DNN
model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(tfidf_train.shape[1],)),  # Input layer com o número de features TF-IDF
    tf.keras.layers.Dense(128, activation='relu'),  # 1ª camada oculta com ativação ReLU
    tf.keras.layers.Dense(64, activation='relu'),   # 2ª camada oculta com ativação ReLU
    tf.keras.layers.Dense(8, activation='softmax')   # Camada de saída com ativação Softmax para classificação multiclasse
])

# Compilar o modelo
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',  # Usar categorical_crossentropy para classes one-hot encoded
              metrics=['accuracy'])

# Treinar o modelo
model.fit(tfidf_train, labels_train, epochs=10, batch_size=32, validation_data=(tfidf_test, labels_test))

# Avaliar o modelo
accuracy = model.evaluate(tfidf_test, labels_test)[1]
print(f'Acurácia do modelo: {accuracy*100}')