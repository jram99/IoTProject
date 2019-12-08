import socket, time, sys

print("Welcome to your home security system\n")

port = 80
otherIP = input("Please enter the ip address of the server: ")

# if __name__ == "main":
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # creates a socket s
    try:
        print("Trying to connect on " + str(otherIP) + ":" + str(port) + "...")
        s.connect((otherIP, port))

    except (socket.timeout, socket.gaierror, TimeoutError):  # throws an exception if the client is unable to connect
        print("\nUnable to connect to that IP address.")
        sys.exit(0)

    print("Connected Successfully")

    while True:
        command = input("Command: ")  # assignes the user entry to a variable
        s.send(b'GET /sensors HTTP/1.1\r\n\r\n')
        time.sleep(1)
        reply = s.recv(1024)
        print(reply)
