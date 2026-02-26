import socket

class Client:
    def __init__(self):
        # Creazione del socket TCP
        # Java: new Socket(nomeServer, portaServer)  |  JS: net.connect(6789, 'localhost')
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_name = "localhost"
        self.server_port = 6789

    def connetti(self):
        # Connessione al server
        # Java: new Socket(nomeServer, portaServer)  |  JS: net.connect(port, host)
        self.client_socket.connect((self.server_name, self.server_port))
        print("CLIENT connesso al server")

    def comunica(self):
        try:
            # Input da tastiera
            messaggio = input("Inserisci la stringa da inviare al server: ")

            # Invio al server
            # Java: outVersoServer.writeBytes(messaggio + '\n')  |  JS: socket.write(msg)
            self.client_socket.send(messaggio.encode())

            # Ricezione risposta dal server
            # Java: inDalServer.readLine()  |  JS: socket.on('data', cb)
            risposta = self.client_socket.recv(1024).decode()
            print(f"Risposta dal server: {risposta}")

        except Exception as e:
            print(f"Errore durante la comunicazione: {e}")

        finally:
            # Chiusura connessione
            # Java: miosocket.close()  |  JS: socket.end()
            self.client_socket.close()
            print("Connessione chiusa")


