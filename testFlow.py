from tensorflow.keras.models import load_model
import numpy as np

# Wczytaj model z pliku
loaded_model = load_model("networkModels/network0.keras")

# Załóżmy, że masz dane wejściowe, które chcesz przewidzieć
input_data = np.random.rand(10, 4)  # Przykładowe dane wejściowe, 10 przykładów, każdy z 4 zmiennymi
print(input_data)
# Wykonaj predykcję
# predictions = loaded_model.predict(input_data)

# print(predictions)