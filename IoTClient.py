import socket, time, sys
import threading

print("Welcome to your home security system\n")

port = 80
host = input("Please enter the ip address of the server: ")
loggingOn = False
terminated = False


class clientMain (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      clientHTTP()
      print ("Exiting main client thread")
      

class logger (threading.Thread):
    def __init__(self, httpRequest):
        threading.Thread.__init__(self)
        self.httpRequest = httpRequest
    def run(self):
        logPrint(self.httpRequest)
    
    
def logPrint(httpRequest):
    global host
    global port
    global terminated
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # creates a socket s
        try:
            s.connect((host, port))
        except (socket.timeout, socket.gaierror, TimeoutError):  # throws an exception if the client is unable to connect
            print("\nUnable to connect to that IP address.")
            sys.exit(0)
            
        while not terminated:
            time.sleep(4)
            if loggingOn == True:
                logFile = open("sensors.log", "w+")
                s.send(httpRequest.encode())
                time.sleep(1)
                reply = s.recv(1024)
                reply = reply.decode().split("close\r\n")
                logFile.write(reply[1])

        
def clientHTTP():
    global host
    global port
    global terminated
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # creates a socket s
        try:
            print("Trying to connect on " + str(host) + ":" + str(port) + "...")
            s.connect((host, port))
        except (socket.timeout, socket.gaierror, TimeoutError):  # throws an exception if the client is unable to connect
            print("\nUnable to connect to that IP address.")
            sys.exit(0)
            
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
    
        while not terminated:
            command = input("Command: ")  # assignes the user entry to a variable
            command.upper()
            inputArray = command.split(' ')
            output = ""
            global loggingOn
    
            if inputArray[0] == 'EXIT':
                terminated = True
                print("Ending session...")
                output = b" "
            elif inputArray[0] == 'LIST':
                print("Proximity sensor on front door (0 or 1) - DOOR")
                print("Temperature sensor for lower floor (Fahrenheit) - TEMP")
                print("Outdoor light infront of main door (0 or 1) - LIGHT")
                print("Burgler alarm indicator (0 or 1) - BUZZ")
                output = b" "
            else:
                if inputArray[0] == 'QUERY':
                    if inputArray[1] == 'ALL':
                        output = b'GET /sensors HTTP/1.1\r\n\r\n'
                    elif inputArray[1] == 'DOOR':
                        output = b'GET /sensors/proximity HTTP/1.1\n\r\n'
                    elif inputArray[1] == 'TEMP':
                        output = b'GET /sensors/temperature HTTP/1.1\n\r\n'
                    elif inputArray[1] == 'LIGHT':
                        output = b'GET /sensors/light HTTP/1.1\n\r\n'
                elif inputArray[0] == 'SET':
                    if inputArray[1] == 'ALARM':
                        if inputArray[2] == 0:
                            output = b'PUT /buzz/off HTTP/1.1\n\r\n'
                        elif inputArray[2] == 1:
                            output = b'PUT /buzz/beeps HTTP/1.1\n\r\n'
                    elif inputArray[1] == 'LIGHT':
                        if inputArray[2] == 0:
                            output = b'PUT /light/off HTTP/1.1\n\r\n'
                        elif inputArray[2] == 1:
                            output = b'PUT /light/on HTTP/1.1\n\r\n'
                elif inputArray[0] == 'START':
                    loggingOn = True
                elif inputArray[0] == 'STOP':
                    loggingOn = False
    
                print("Before send")
                s.send(output)
                print("After send, before receive")
                time.sleep(1)
                reply = s.recv(1024)
                print("After receive")
                reply = reply.decode().split("close\r\n")
                print(reply[1])
    
    # End session and cleanup
    s.close()
    sys.exit(0)
    
        
mainThread = clientMain()
logThread = logger('GET /sensors HTTP/1.1\r\n\r\n')
    
mainThread.start()
logThread.start()