import socket, time, sys, email, smtplib, ssl, threading


print("Welcome to your home security system\n")

port = 80
#otherIP = input("Please enter the ip address of the server: ")
otherIP = "10.17.110.123"
email_password = "P@$$word1!"
sender = "comp342gccf19@gmail.com"
recipient = "ramjac13@gmail.com"
alarm = False
logging = False
EXIT_PROGRAM = False
actuator_password = "Turtles"

msg1 = "From: me \r\nTo: you \r\nSubject: subject \r\n\r\nALERT ALERT! YOUR DOOR IS OPEN!\r\n"
msg2 = "From: me \r\nTo: you \r\nSubject: subject \r\n\r\nDoor closed again.\r\n"


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
    global alarm
    global logging
    global EXIT_PROGRAM
    while not EXIT_PROGRAM:
        command = input("Command: ").upper()  # assignes the user entry to a variable
        inputArray = command.split(' ')
        timer = 1
        lightOn = False
        receivesBack = False

        if inputArray[0] == 'LIST':
            print("Use the following prompts for their respective actions:")
            print("1. LIST -                 List hardware (and options) available")
            print("2. QUERY <sensor> -       Query value of specific sensor (from LIST)")
            print("3. QUERY ALL -            Query values of all sensors")
            print("4. SET LIGHT <val> -      Set value of outdoor lights (from LIST)")
            print("5. SET ALARM <val> -      Set alarm condition")
            print("6. START -                Start logging sensor data")
            print("7. STOP -                 Stop logging sensor data")
            print("8. EXIT -                 End current session\n")
            
            print("Proximity sensor on front door (0 or 1) - DOOR")
            print("Temperature sensor for lower floor (Fahrenheit) - TEMP")
            print("Outdoor light in front of main door (0 or 1) - LIGHT")
            print("Set alarm ON to notify every few seconds if door is open")
            print("Start logging sensor data (START) - writes to log file\n")
        elif inputArray[0] == 'EXIT':
            print("Ending session...")
            EXIT_PROGRAM = True
        elif inputArray[0] == 'START':
            print("Starting log")
            logging = True
        elif inputArray[0] == 'STOP':
            print("Ended log")
            logging = False
        else:
            if inputArray[0] == 'QUERY':
                if inputArray[1] == 'ALL':
                    s.send(b'GET /sensors HTTP/1.1\r\n\r\n')
                    receivesBack = True
                elif inputArray[1] == 'DOOR':
                    s.send(b'GET /sensors/proximity HTTP/1.1\n\r\n')
                    receivesBack = True
                elif inputArray[1] == 'TEMP':
                    s.send(b'GET /sensors/temperature HTTP/1.1\n\r\n')
                    receivesBack = True
                elif inputArray[1] == 'LIGHT':
                    print("Light is " + str(lightOn))
                else:
                    print("Invalid Input")
                    break
    
            elif inputArray[0] == 'SET':
                if inputArray[1] == 'ALARM':
                    if inputArray[2] == 'ON':
                        #here is part of the problem
                        alarm = True
                        s.send(b'PUT /buzz/off HTTP/1.1\n\r\n')
                        #output = b'PUT /buzz/off HTTP/1.1\n\r\n'
                    elif inputArray[2] == 'OFF':
                        alarm = False
                        s.send(b'PUT /led/off HTTP/1.1\n\r\n')
                        mailer = smtplib.SMTP_SSL('smtp.gmail.com',465)
                        mailer.ehlo()
                        mailer.login(sender, email_password)
                        mailer.sendmail(sender, recipient, msg2)
                        mailer.close()
                        print("Alarm deactivated")
                elif inputArray[1] == 'LIGHT':
                    if inputArray[2] == '0':
                        s.send(b'PUT /led/off HTTP/1.1\n\r\n')
                        lightOn = False
                        receivesBack = True
                    elif inputArray[2] == '1':
                        s.send(b'PUT /led/on HTTP/1.1\n\r\n')
                        lightOn = True
                        receivesBack = True
                    else:
                        print("Invalid Input")
                        break
        if receivesBack:
            time.sleep(timer)
            reply = s.recv(1024)
            time.sleep(1)
            reply = reply.decode().split("close\r\n")
            print(reply[1])
            
    print("Session terminated")
    s.close()
    sys.exit(0)

# End session and cleanup
def setAlarm():
    #here is part of the problem
    global alarm
    global EXIT_PROGRAM
    while not EXIT_PROGRAM:
        if alarm:
            s.send(b'GET /sensors HTTP/1.1\r\n\r\n')
            time.sleep(5)
            data = s.recv(1024)
            data = data.decode()
            if '"proximity": 0' in data:
                s.send(b'PUT /buzz/beeps HTTP/1.1\n\r\n')
                s.send(b'PUT /led/on HTTP/1.1\n\r\n')
                data = s.recv(1024)
                print("Door is open!")
                mailer = smtplib.SMTP_SSL('smtp.gmail.com',465)
                mailer.ehlo()
                mailer.login(sender, email_password)
                mailer.sendmail(sender, recipient, msg1)
                mailer.close()


def logData():
    global logging
    global EXIT_PROGRAM
    while not EXIT_PROGRAM:
        if logging:
            f = open("data.txt", 'w+')
            s.send(b'GET /sensors HTTP/1.1\r\n\r\n')
            data = s.recv(1024)
            data = data.decode().split("close\r\n")
            data = data[1]
            log = "" + data + ""
            f.write(log)
            print(log)
            f.flush()
            f.close()
            time.sleep(5)


#initiates the two threads
t = threading.Thread(target=getinput, args=())
t2 = threading.Thread(target=setAlarm, args=())
t3 = threading.Thread(target=logData, args=())
#starts the two threads
t.start()
t2.start()
t3.start()