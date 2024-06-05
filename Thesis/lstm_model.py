# -*- coding: utf-8 -*-
"""LSTM Model

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QT77baZmhiCKLUTyxJDHJ1Sc818BQGoV
"""

import pandas as pd
import numpy as np

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.optimizers import Nadam
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator



df = pd.read_csv("Math Scores.csv",
                 index_col=('Date'),
                 parse_dates=True)

df.head()

train = df.iloc[:20]
test = df.iloc[21:]

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(train['Current Score'].values.reshape(-1, 1))
scaled_train = scaler.transform(train['Current Score'].values.reshape(-1, 1))
scaled_test = scaler.transform(test['Current Score'].values.reshape(-1, 1))

n_input = 1
n_features = 1
generator = TimeseriesGenerator(scaled_train,
								scaled_train[:, :n_features],
								length=n_input,
								batch_size=1)

model = Sequential()
model.add(LSTM(100, activation='relu',
               input_shape=(n_input, n_features)))
model.add(Dense(1))
model.summary()
model.compile(optimizer=Nadam(clipnorm=1), loss='mse', )
model.fit(generator, epochs=100)

input_data = scaled_train[0:1]
input_data = input_data.reshape((1, n_input, n_features))



def predict_score():
    prediction = model.predict(input_data)

    predicted_score = scaler.inverse_transform(prediction)

    print("Predicted Score: ", predicted_score[0][0])

