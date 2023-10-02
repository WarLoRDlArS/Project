import socket
import threading

def portSearch(ServerSock,ServerIP):
    port=1025
    while port<66000:
        try:
            ServerSock.bind((ServerIP,port))
            break
        except:
            port+=1
    return port

def SendMessage():
    pass

def RecvMessage():
    pass

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as serverSocket:
    ServerIP = socket.gethostbyname(socket.gethostname()) 
    #bind to the port
    #this function will also bind the socket
    ServerPort= portSearch(serverSocket,ServerIP)
    print(f"IP:{ServerIP}\tPort:{ServerPort}")

