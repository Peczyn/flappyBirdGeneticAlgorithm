import socket

HOST = '127.0.0.1'  # Adres localhost
PORT = 65432        # Port do komunikacji

# Tworzenie gniazda
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # Nawiązanie połączenia

    # Symulacja gry
    while True:
        # Wysłanie danych do plikNeuron
        s.sendall(b'jump_request')

        # Odbiór odpowiedzi od plikNeuron
        odpowiedz = s.recv(1024).decode()
        print("Odpowiedź od plikNeuron:", odpowiedz)

        # Symulacja wykonania skoku lub nieskoku na podstawie odpowiedzi
        if odpowiedz == 'True':
            print("Wykonaj skok!")
        else:
            print("Nie wykonuj skoku.")
