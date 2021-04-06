# -*- coding: utf-8 -*-
 
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', 8888))
sock.listen()
print(sock.getsockname())

# blocking
conn, addr = sock.accept()

print('connection from ', addr)

while True:
    data = conn.recv(1024)
    data = data.strip()
    if data == b'quit': break
    if not data: break
    print(b'receive: ' + data)
    conn.sendall(b'reply:' + data + b'\n')


sock.close()
