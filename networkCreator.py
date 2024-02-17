from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np

for i in range(100):
     model = Sequential()
     model.add(Dense(8, input_shape=(4,), activation='relu', ))
     # model.add(Dense(8, activation='relu'))
     model.add(Dense(1, activation='sigmoid'))
     model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
     model.save(f"networkModels/network{i}.keras")

#model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
#to do kompilacji przed uzyciem modelu