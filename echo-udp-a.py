# -*- coding: utf-8 -*-
 
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', 8888))
print(sock.getsockname())
sock.sendto(b'Hello', ('0.0.0.0', 8889))
sock.close()
