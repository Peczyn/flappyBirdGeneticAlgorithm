import tensorflow as tf

# Sprawdzenie wersji TensorFlow
print("Wersja TensorFlow:", tf.__version__)

from keras.datasets import mnist

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
train_images.shape

#ARCHITEKTURA SIECI
from keras import models
from keras import layers

network = models.Sequential()
network.add(layers.Dense(512, activation='relu', input_shape=(28 * 28,)))
network.add(layers.Dense(10, activation='softmax'))
#ARCHITEKTURA SIECI


#TRENING SIECI
network.compile(optimizer='rmsprop',
                loss='categorical_crossentropy',
                metrics=['accuracy'])
#TRENING SIECI

#PROCESSING DANYCH TAK ABY BYLY W OCZEKIWANIE FORMIE ORAZ ICH WARTOSCI BYLY OD 0-1
# TODO
# Przetwarzanie danych treningowych
train_images = train_images.reshape((60000, 28 * 28))
train_images = train_images.astype('float32') / 255

# Przetwarzanie danych testowych
test_images = test_images.reshape((10000, 28 * 28))
test_images = test_images.astype('float32') / 255
#PROCESSING DANYCH TAK ABY BYLY W OCZEKIWANIE FORMIE ORAZ ICH WARTOSCI BYLY OD 0-1

#TU KONWERSJA DANYCH BO UZYWAMY CATEGORICAL_CROSSENTROPY
from keras.utils import to_categorical

train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)
#TU KONWERSJA DANYCH BO UZYWAMY CATEGORICAL_CROSSENTROPY


#TODO: dopasowywanie modelu  /// DOPASOWYWANIE NA ZESTAWIE SZKOLENIOWYM
network.fit(train_images, train_labels, epochs = 5, batch_size = 128)

#TEST NA ZESTAWIE TESTOWYM
test_loss, test_acc = network.evaluate(test_images, test_labels)
print('test_acc:', test_acc)