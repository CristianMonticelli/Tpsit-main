import socket

def main():
    # 1️⃣ Creazione del socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_name = "localhost"
    server_port = 6789

    try:
        # 2️⃣ Connessione al server
        client_socket.connect((server_name, server_port)) #java new Socket(nomeServer, portaServer);
        print("CLIENT connesso al server")

        # 3️⃣ Input da tastiera
        messaggio = input("Inserisci la stringa da inviare al server: ")

        # 4️⃣ Invio al server (serve convertire in byte)
        client_socket.send(messaggio.encode())

        # 5️⃣ Ricezione risposta dal server
        risposta = client_socket.recv(1024).decode()
        print("Risposta dal server:", risposta)

    except Exception as e:
        print("Errore durante la comunicazione:", e)

    finally:
        # 6️⃣ Chiusura connessione
        client_socket.close()
        print("Connessione chiusa")

if __name__ == "__main__":
    main()
