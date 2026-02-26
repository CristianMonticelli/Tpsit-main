import socket

class Server:
    def __init__(self):
        # Java: ServerSocket server = new ServerSocket(6789)
        # JS:   const server = net.createServer()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket = None

    def attendi(self):
        # Lega il socket alla porta e mette in ascolto
        # Java: new ServerSocket(6789)  |  JS: server.listen(6789)
        self.server_socket.bind(('', 6789))
        self.server_socket.listen(1)
        print("SERVER in ascolto sulla porta 6789...")

        # Blocca finché un client non si connette
        # Java: Socket client = server.accept()  |  JS: callback di net.createServer
        self.client_socket, addr = self.server_socket.accept()
        print(f"Client connesso da: {addr}")

        # Chiudo il ServerSocket per inibire altri client (comunicazione Unicast)
        # Java: server.close()  |  JS: server.close()
        self.server_socket.close()

    def comunica(self):
        try:
            # Ricezione stringa dal client
            # Java: inDalClient.readLine()  |  JS: socket.on('data', cb)
            stringa_ricevuta = self.client_socket.recv(1024).decode()
            print(f"Ricevuto dal client: {stringa_ricevuta}")

            # Elaborazione: converti in maiuscolo
            # Java: stringa.toUpperCase()  |  JS: str.toUpperCase()
            stringa_modificata = stringa_ricevuta.upper()

            # Invio risposta al client
            # Java: outVersoClient.writeBytes(stringa + '\n')  |  JS: socket.write(str)
            self.client_socket.send(stringa_modificata.encode())
            print(f"Inviato al client: {stringa_modificata}")

        except Exception as e:
            print(f"Errore durante la comunicazione: {e}")

        finally:
            # Chiusura connessione col client
            # Java: client.close()  |  JS: socket.end()
            self.client_socket.close()
            print("Connessione chiusa")


