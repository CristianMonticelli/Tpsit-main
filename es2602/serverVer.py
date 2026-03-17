import socket

#server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket = None
server_socket.bind(('', 6789))
server_socket.listen(1)
server_socket.accept()
stringa_ricevuta = client_socket.recv(1024)
stringa_modificata = 'CIAO'
client_socket.send(stringa_modificata)
client_socket.close()