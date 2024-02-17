import socket
import numpy
import keras
import tensorflow

HOST = '127.0.0.1'  # Adres localhost
PORT = 65432  # Port do komunikacji

# Tworzenie gniazda
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))  # Przypisanie gniazda do adresu i portu
    s.listen()  # Nasłuchiwanie połączeń

    # Akceptowanie połączenia
    conn, addr = s.accept()
    with conn:
        print('Połączono z', addr)
        while True:
            # Odbiór żądania od plikGame
            data = conn.recv(1024)
            if not data:
                break
            request = data.decode()

            numbers = request.split(',')

            # Wybierz ostatnie cztery liczby
            last_four_numbers = numbers[-4:]

            # Przekonwertuj te cztery liczby na floaty
            float_numbers = [float(num) for num in last_four_numbers]

            # Stwórz tablicę numpy z tymi liczbami
            input_data = numpy.array([float_numbers])


            model = keras.models.load_model(f"networkModels/network{request[0]}.keras")
            model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
            predictions = model.predict(input_data, ver)
            # print(predictions)

            # Tutaj należy umieścić logikę, która określa czy gracz powinien wykonać skok
            # W tym przykładzie symulujemy odpowiedź losową

            should_jump = False
            if predictions > 0.5:
                should_jump = True

            # Wysłanie odpowiedzi do plikGame
            conn.sendall(str(should_jump).encode())
