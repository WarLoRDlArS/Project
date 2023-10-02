import socket
import threading
import sys
import time

switchCase = {
    1 : "Sign In",
    2: "Log In"
}

def ClientConnect(serverIP,ServerPort):
    """This function is used to Connect Client to the server
    """
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as clientConn:
        try:
            clientConn.connect((serverIP,ServerPort))  
            print(clientConn)
            return clientConn
        except:
            print("Couldnt Connect to server") 
            sys.exit()

def sendMessage(ClientConn,message): 
    while True: 
        print("Enter message: ")
        message=input()
        if message.lower() == 'exit':
            break
        try: 
            ClientConn.send(message.encode('utf-8'))
        except:
            print("Couldnt Send Message: " + message)  
        time.sleep(1)

def recMessage(clientSock):
    while True:
        try:
            messageBuffer = b''
            while True:
                chunk = clientSock.recv(1024)
                if not chunk:
                    break
                messageBuffer += chunk

            if messageBuffer:
                message = messageBuffer.decode('utf-8')
                print(message)
                #return message

        except Exception as e:
            print(f"Error in receiving message: {str(e)}")
            break

if __name__=="__main__":
    print("Enter Server IP:")
    serverIP=input()
    print("Enter Server Port:")
    serverPort=int(input())
    clientconn=ClientConnect(serverIP,serverPort)
    try:
        send = threading.Thread(target=sendMessage, args=(clientconn, "hello"))
        recv = threading.Thread(target=recMessage, args=(clientconn,))
        send.start()
        recv.start()
    except:
        print("Couldnt create threads")
    print("What Would You Like To Do: ")
    for x,y in switchCase.items():
        print(x, y)
