# -*- coding: utf-8 -*-
 
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#sock.bind(('0.0.0.0', 8889))
sock.connect(('0.0.0.0', 8888))
sock.sendall(b'hello')
data = sock.recv(1024)
data = data.strip()
print(b'echo: ' + data)
sock.close()
