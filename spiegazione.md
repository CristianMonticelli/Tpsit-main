Perfetto 👍 Rifacciamo lo stesso esercizio del client TCP, ma questa volta in Python invece che in Java.

L’obiettivo è lo stesso del libro:

Il client si connette a un server (localhost, porta 6789)

Legge una stringa da tastiera

La invia al server

Riceve la risposta

Chiude la connessione

🔹 1. Concetti base (equivalente Java → Python)

In Java usavi:

Socket

DataOutputStream

BufferedReader

close()

In Python useremo il modulo:

import socket


E lavoreremo con:

socket.socket() → crea il socket

connect() → connessione al server

send() → invio dati

recv() → ricezione dati

close() → chiusura connessione

🔹 2. Variabili del client

Come nel libro:

nome server → "localhost"

porta → 6789

🔹 3. Codice completo del Client TCP in Python
import socket

def main():
    # 1️⃣ Creazione del socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_name = "localhost"
    server_port = 6789

    try:
        # 2️⃣ Connessione al server
        client_socket.connect((server_name, server_port))
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

🔹 4. Spiegazione passo per passo
🔸 socket.AF_INET

Indica che usiamo IPv4.

🔸 socket.SOCK_STREAM

Indica protocollo TCP (come in Java).

🔸 connect((host, porta))

Equivalente a:

new Socket(nomeServer, portaServer);

🔸 send()

Invia dati al server.
⚠ In Python i dati devono essere in byte, quindi:

messaggio.encode()

🔸 recv(1024)

Riceve fino a 1024 byte dal server.
Poi convertiamo in stringa con:

.decode()

🔸 close()

Chiude il socket (come close() in Java).

🔹 5. Differenze principali rispetto a Java
Java	Python
Socket	socket.socket()
getInputStream()	recv()
getOutputStream()	send()
try/catch	try/except
gestione stream	gestione diretta byte

In Python il codice è molto più compatto.