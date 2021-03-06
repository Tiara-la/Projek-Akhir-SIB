# -*- coding: utf-8 -*-
"""Model_Capstone.ipynb

Automatically generated by Colaboratory.

Original file is located at

    https://colab.research.google.com/drive/1-kVtswFcXjqy7-EMLUQQ4kiJDFNhHMR8

"""

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt

data = pd.read_csv("/content/sample_data/Human Activity.csv")
data

data.info()

data

data.describe()

data = data.drop("Timestamp", axis=1)

data = data.drop("Kegiatan lain (Opsional)", axis=1)

df = data.sample(frac=1, random_state=42)
df

x = df[['Usia', 'Kegiatan 1', 'Kegiatan 2', 'Kegiatan 3', 'Kegiatan 4', 'Kegiatan 5']]
y = df[['Hobi', 'Gender', 'Rentang Usia', 'Pekerjaan (jika masih bersekolah bisa diisi siswa/mahasiswa)']]

# Membagi menjadi 80% data train dan 20% data validasi
train_indices = int(0.8 * df.shape[0])
x_train, x_val, y_train, y_val = (
    x[:train_indices],
    x[train_indices:],
    y[:train_indices],
    y[train_indices:]
)
 
print(x, y)

import nltk
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings
warnings.filterwarnings('ignore')

features=[]

for i in range(df.shape[0]):
    features.append(" ".join(list(df.iloc[i].values)))

lem=nltk.WordNetLemmatizer()
corpus=[]

for i in range(len(features)):
    review=re.sub('[^a-zA-Z]',' ',features[i])
    review=review.lower()
    review=review.split()
    review=' '.join(review)
    corpus.append(review)

df['features']=corpus
df.head()

tf = TfidfVectorizer()
tfidf_matrix=tf.fit_transform(df['features'])
tfidf_matrix.shape

tfidf_matrix.todense()

cosine_sim = cosine_similarity(tfidf_matrix) 
cosine_sim

import numpy as np
def activity_recommendations(Hobi):
    data_index=df[[Hobi in name for name in df["Hobi"]]].index[0]
    similarity_score=list(enumerate(cosine_sim[data_index]))
    similarity_score=sorted(similarity_score,key=lambda x:x[1],reverse=True)
    similarity_score=similarity_score[1:6]
    activity_indices=[idx[0] for idx in similarity_score]
    return df['Hobi'][activity_indices]

data[data.Hobi.eq('Travelling')]


activity_recommendations('Travelling')


