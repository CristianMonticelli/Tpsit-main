import socket

#client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_name = "localhost"
server_port = 6789
client_socket.connect((server_name, server_port))
messaggio = "ciao"
client_socket.send(messaggio.encode())
risposta = client_socket.recv(1024)
client_socket.close()