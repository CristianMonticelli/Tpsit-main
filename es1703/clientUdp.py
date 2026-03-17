import socket

class UDPClient:
    def __init__(self, host='localhost', port=6789, timeout=3):
        self.server = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(timeout)

    def send_and_receive(self, message):
        try:
            self.sock.sendto(message.encode(), self.server)  # invia datagram
            data, addr = self.sock.recvfrom(4096)            # attende risposta
            print(f"Risposta da {addr}: {data.decode()}")
        except socket.timeout:
            print("Timeout: nessuna risposta dal server")
        except Exception as e:
            print(f"Errore: {e}")

    def close(self):
        try:
            self.sock.close()
        except Exception:
            pass

if __name__ == '__main__':
    c = UDPClient()
    try:
        while True:
            msg = input("Messaggio (vuoto per uscire): ")
            if not msg:
                break
            c.send_and_receive(msg)
    finally:
        c.close()