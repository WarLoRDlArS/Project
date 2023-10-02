import socket
import threading
from Main import *

def portSearch(ServerSock,ServerIP):
    port=1026
    while port<66000:
        try:
            ServerSock.bind((ServerIP,port))
            break
        except:
            port+=1
    return port

def SendMessage(ClientSock,message):
    while True: 
        try: 
            ClientSock.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Exception in sending message:{message}") 
            print(e)

def RecvMessage(ClientSock):
        while True:
            try:
                messageBuffer=b''
                while True:
                    chunk=ClientSock.recv(1024)
                    if not chunk:
                        break
                    messageBuffer+=chunk
                if not messageBuffer:
                    break
                message=messageBuffer.decode('utf-8')
                print(message)
                return message
                
            except Exception as e:
                print("Exception in recieveing message\n\n")
                print(f"Error: {str(e)}") 
    


with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as serverSocket:
    ServerIP = socket.gethostbyname(socket.gethostname()) 
    #bind to the port
    #this function will also bind the socket
    ServerPort= portSearch(serverSocket,ServerIP)
    try:
        serverSocket.bind((ServerIP,ServerPort))
    except:
        print("Server already binded")

    print(f"IP:{ServerIP}\tPort:{ServerPort}")

    serverSocket.listen()
    clientSocket,Clientadd=serverSocket.accept()
    print(f"Client {Clientadd} connected")
    
    try:
        recieve=threading.Thread(target=RecvMessage,args=(clientSocket,))
        send=threading.Thread(target=SendMessage,args=(clientSocket,"hello from server"))
        recieve.start()
        send.start()
    except:
        print("Couldnt create threads")
    print("Hello")
