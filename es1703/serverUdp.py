import socket
import threading

class UDPServer:
    def __init__(self, host='', port=6789):
        self.addr = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.running = False

    def start(self):
        self.sock.bind(self.addr)
        self.running = True
        print(f"UDP server in ascolto su {self.addr}...")
        try:
            while self.running:
                data, client = self.sock.recvfrom(4096)  # riceve datagram
                if not data:
                    continue
                # gestisce il pacchetto in un thread per non bloccare il loop
                threading.Thread(target=self.handle_packet, args=(data, client), daemon=True).start()
        except KeyboardInterrupt:
            print("Arresto server (KeyboardInterrupt)")
        finally:
            self.stop()

    def handle_packet(self, data, client):
        try:
            text = data.decode(errors='ignore')
            print(f"[{client}] ricevuto: {text}")
            resp = text.upper()  # elaborazione: uppercase
            self.sock.sendto(resp.encode(), client)  # invia risposta
        except Exception as e:
            print(f"Errore con {client}: {e}")

    def stop(self):
        self.running = False
        try:
            self.sock.close()
        except Exception:
            pass
        print("Server UDP fermato")

if __name__ == '__main__':
    srv = UDPServer(host='', port=6789)
    srv.start()