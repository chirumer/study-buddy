# simple client send and receive

import socket

PORT = 5200

sock = socket.socket()

sock.connect(('127.0.0.1', PORT))

sock.send('hello world'.encode())
print(sock.recv(1024).decode())

sock.close()
