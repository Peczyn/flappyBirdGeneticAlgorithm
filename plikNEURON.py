import socket

HOST = '127.0.0.1'  # Adres localhost
PORT = 65432        # Port do komunikacji

# Tworzenie gniazda
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))   # Przypisanie gniazda do adresu i portu
    s.listen()             # Nasłuchiwanie połączeń

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
            print("Otrzymane żądanie od plikGame:", request)

            # Tutaj należy umieścić logikę, która określa czy gracz powinien wykonać skok
            # W tym przykładzie symulujemy odpowiedź losową
            import random
            randomnum = random.randint(1,20)
            should_jump = False
            if randomnum==1:
                should_jump=True


            # Wysłanie odpowiedzi do plikGame
            conn.sendall(str(should_jump).encode())
