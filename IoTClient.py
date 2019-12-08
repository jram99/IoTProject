import socket, time

print("Welcome to your home security system\n")


#if __name__ == "main":
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #creates a socket s
    s.connect(("10.17.111.161", 80))
    s.send(b'GET /sensors HTTP/1.1\r\n\r\n')
    time.sleep(1)
    reply = s.recv(1024)
    print(reply)