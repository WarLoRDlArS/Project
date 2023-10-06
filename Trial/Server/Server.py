import socket
import threading
import sys

def portSearchBind(ServerSock, ServerIP):
    port = 1026
    while port < 66000:
        try:
            ServerSock.bind((ServerIP, port))
            break
        except:
            port += 1
    return port

def SendMessage(ClientSock, message):
    while True:
        try:
            ClientSock.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Exception in sending message: {message}")
            print(e)
            break

def RecvMessage(ClientSock):
    while True:
        try:
            messageBuffer = b''
            while True:
                chunk = ClientSock.recv(1024)
                if not chunk:
                    break
                messageBuffer += chunk
            if not messageBuffer:
                break
            message = messageBuffer.decode('utf-8')
            print(message)

        except Exception as e:
            print("Exception in receiving message\n\n")
            print(f"Error: {str(e)}")
            break

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
        ServerIP = socket.gethostbyname(socket.gethostname())
        ServerPort = portSearchBind(serverSocket, ServerIP)

        print(f"IP: {ServerIP}\tPort: {ServerPort}\n")

        serverSocket.listen()
        while True:
            clientSocket, Clientadd = serverSocket.accept()
            print(f"Client {Clientadd} connected\n")

            try:
                recieve = threading.Thread(target=RecvMessage, args=(clientSocket,))
                send = threading.Thread(target=SendMessage, args=(clientSocket, "hello from server"))
                
                recieve.start()
                send.start()

                recieve.join()  # Wait for receive thread to finish
                send.join()  # Wait for send thread to finish

            except Exception as e:
                print(f"Couldn't create threads\nException: {e}")
