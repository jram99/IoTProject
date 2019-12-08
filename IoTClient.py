import socket, time, sys

print("Welcome to your home security system\n")

port = 80
otherIP = input("Please enter the ip address of the server: ")

# if __name__ == "main":
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # creates a socket s
    terminated = False
    
    try:
        print("Trying to connect on " + str(otherIP) + ":" + str(port) + "...")
        s.connect((otherIP, port))

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
        ouput = ""
        
        if inputArray[0] == 'EXIT':
            terminated = True
            print("Ending session...")
        elif inputArray[0] == 'LIST':
            print("Proximity sensor on front door (0 or 1) - DOOR")
            print("Temperature sensor for lower floor (Fahrenheit) - TEMP")
            print("Outdoor light infront of main door (0 or 1) - LIGHT")
            print("Burgler alarm indicator (0 or 1) - BUZZ")
        elif inputArray[0] == 'QUERY':
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
        
        s.send(output)
        time.sleep(1)
        reply = s.recv(1024)
        print(reply)
        
print("Session terminated")
