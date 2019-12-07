import socket
import time


#if __name__ == "main":
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("10.17.111.161", 80))
s.send(b'GET /sensors HTTP/1.1\r\n\r\n')
time.sleep(1)
reply = s.recv(1024)
print(reply)