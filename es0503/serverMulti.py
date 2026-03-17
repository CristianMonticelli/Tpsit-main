import socket
import threading

class ThreadedServer:
    def __init__(self, host='', port=6789):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # crea TCP socket
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # riuso indirizzo
        self.running = False

    def start(self):
        self.server_socket.bind((self.host, self.port))  # lega alla porta
        self.server_socket.listen(5)                      # mette in ascolto (backlog 5)
        self.running = True
        print(f"SERVER multithread in ascolto su {self.host or '0.0.0.0'}:{self.port}...")
        try:
            while self.running:
                try:
                    client_sock, addr = self.server_socket.accept()  # accetta connessione (bloccante)
                except OSError:
                    break
                print(f"Connessione da {addr}")
                t = threading.Thread(target=self.handle_client, args=(client_sock, addr), daemon=True)  # nuovo thread per client
                t.start()
        except KeyboardInterrupt:
            print("Arresto server (KeyboardInterrupt)")
        finally:
            self.stop()

    def handle_client(self, client_sock, addr):
        try:
            while True:
                data = client_sock.recv(1024)  # ricevi dati
                if not data:
                    break  # client chiuso
                text = data.decode(errors='ignore')
                print(f"[{addr}] ricevuto: {text}")
                resp = text.upper()  # elaborazione: uppercase
                client_sock.send(resp.encode())  # invia risposta
        except Exception as e:
            print(f"Errore con {addr}: {e}")
        finally:
            client_sock.close()  # chiudi socket client
            print(f"Connessione {addr} chiusa")

    def stop(self):
        self.running = False
        try:
            self.server_socket.close()  # chiudi socket server
        except Exception:
            pass
        print("Server fermato")

if __name__ == '__main__':
    srv = ThreadedServer(host='', port=6789)
    try:
        srv.start()
    except Exception as e:
        print(f"Errore in avvio server: {e}")
        srv.stop()