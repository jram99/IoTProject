import socket, time, sys, email, smtplib, ssl, threading


from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

print("Welcome to your home security system\n")

port = 80
otherIP = input("Please enter the ip address of the server: ")
password = "Password1$"
sender = "comp342gccf19@gmail.com"
recipient = "ramjac13@gmail.com"
alarm = False

# if __name__ == "main":
#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # creates a socket s
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# try:
#     print("Trying to connect on " + str(otherIP) + ":" + str(port) + "...")
#     s.connect((otherIP, port))
#
# except (socket.timeout, socket.gaierror, TimeoutError):  # throws an exception if the client is unable to connect
#     print("\nUnable to connect to that IP address.")
#     sys.exit(0)

print("Trying to connect on " + str(otherIP) + ":" + str(port) + "...")
s.connect((otherIP, port))
print("Connected Successfully\n")

print("Use the following prompts for their respective actions:")
print("1. LIST -                 List hardware (and options) available")
print("2. QUERY <sensor> -       Query value of specific sensor (from LIST)")
print("3. QUERY ALL -            Query values of all sensors")
print("4. SET LIGHT <val> -      Set value of outdoor lights (from LIST)")
print("5. SET ALARM <val> -      Set alarm condition")
print("6. START -                Start logging sensor data")
print("7. STOP -                 Stop logging sensor data")
print("8. EXIT -                 End current session")

def getinput():
    while True:
        command = input("Command: ").upper()  # assignes the user entry to a variable
        inputArray = command.split(' ')
        timer = 1

        if inputArray[0] == 'LIST':
            print("Proximity sensor on front door (0 or 1) - DOOR")
            print("Temperature sensor for lower floor (Fahrenheit) - TEMP")
            print("Outdoor light in front of main door (0 or 1) - LIGHT")
            print("Burglar alarm indicator (0 or 1) - BUZZ")
        elif inputArray[0] == 'EXIT':
            print("Ending session...")
            print("Session terminated")
            s.close()
            sys.exit(0)
        elif inputArray[0] == 'QUERY':
            if inputArray[1] == 'ALL':
                s.send(b'GET /sensors HTTP/1.1\r\n\r\n')
            elif inputArray[1] == 'DOOR':
                s.send(b'GET /sensors/proximity HTTP/1.1\n\r\n')
            elif inputArray[1] == 'TEMP':
                s.send(b'GET /sensors/temperature HTTP/1.1\n\r\n')
            elif inputArray[1] == 'LIGHT':
                s.send(b'GET /sensors/light HTTP/1.1\n\r\n')
            else:
                print("Invalid Input")
                break

        elif inputArray[0] == 'SET':
            if inputArray[1] == 'ALARM':
                if inputArray[2] == 'ON':
                    alarm = True


                    #output = b'PUT /buzz/off HTTP/1.1\n\r\n'
                elif inputArray[2] == '1':
                    s.send(b'PUT /buzz/beeps HTTP/1.1\n\r\n')
            elif inputArray[1] == 'LIGHT':
                if inputArray[2] == '0':
                    s.send(b'PUT /led/off HTTP/1.1\n\r\n')
                elif inputArray[2] == '1':
                    s.send(b'PUT /led/on HTTP/1.1\n\r\n')
                else:
                    print("Invalid Input")
                    break
        elif inputArray[0] == 'START':
            f = open("data.txt", 'w+')
            while inputArray[0] != 'STOP':
                s.send(b'GET /sensors HTTP/1.1\r\n\r\n')
                timer = 5
                time.sleep(5)
                data = s.recv(1024)
                data = data.decode().split("close\r\n")
                data = data[1]

                log = "" + data + ""
                f.write(log)
                print(log)
                f.flush()
            f.close()
        else:
            print("Invalid Input")
            break
        time.sleep(timer)
        reply = s.recv(1024)
        reply = reply.decode().split("close\r\n")
        print(reply[1])

# End session and cleanup
def setAlarm():
    if alarm:
        alert = False
        while not alert:
            s.send(b'GET /sensors HTTP/1.1\r\n\r\n')
            time.sleep(5)
            data = s.recv(1024)
            data = data.decode()
            if '"proximity": 0' in data:
                s.send(b'PUT /buzz/beeps HTTP/1.1\n\r\n')
                s.send(b'PUT /led/on HTTP/1.1\n\r\n')
                print("Door is open!")
                alert = True



#initiates the two threads
t = threading.Thread(target=getinput, args=())
t2 = threading.Thread(target=setAlarm, args=())
#starts the two threads
t.start()
t2.start()
