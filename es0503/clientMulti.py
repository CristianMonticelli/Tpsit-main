import socket

class Client:
    def __init__(self, host='localhost', port=6789):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        print(f"Connesso a {self.host}:{self.port}")

    def interactive(self):
        try:
            while True:
                msg = input("Messaggio (digita 'exit' per chiudere): ")
                if msg.lower() in ('exit', 'quit'):
                    break
                if not msg:
                    continue
                self.sock.send(msg.encode())
                resp = self.sock.recv(4096).decode(errors='ignore')
                print(f"Risposta: {resp}")
        except Exception as e:
            print(f"Errore: {e}")
        finally:
            self.close()

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None
            print("Connessione chiusa")

if __name__ == '__main__':
    c = Client()
    c.connect()
    c.interactive()