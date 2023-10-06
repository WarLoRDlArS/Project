import socket
import threading
import sys
import time

switchCase = {
    1: "Sign In",
    2: "Log In"
}

def ClientConnect(serverIP, ServerPort):
    """This function is used to Connect Client to the server
    """
    clientConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        clientConn.connect((serverIP, ServerPort))
        print("Connected to the server")
        return clientConn
    except Exception as e:
        print("Couldn't Connect to the server")
        print(f"Exception {e}")
        sys.exit()

def sendMessage(ClientConn):
    while True:
        print("Enter message: ")
        message = input()
        if message.lower() == 'exit':
            break
        try:
            ClientConn.send(message.encode('utf-8'))
        except Exception as e:
            print("Couldn't Send Message: " + message)
            print(f"Exception {e}")
            break
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

        except Exception as e:
            print(f"Error in receiving message: {str(e)}")
            break

if __name__ == "__main__":
    print("Enter Server IP:")
    serverIP = input()
    print("Enter Server Port:")
    serverPort = int(input())
    clientconn = ClientConnect(serverIP, serverPort)

    try:
        send = threading.Thread(target=sendMessage, args=(clientconn,))
        recv = threading.Thread(target=recMessage, args=(clientconn,))
        send.start()
        recv.start()
        send.join()  # Wait for send thread to finish
        clientconn.close()  # Close the socket after sending is done
        recv.join()  # Wait for receive thread to finish

    except Exception as e:
        print("Error:", str(e))
        print("Couldn't create threads")

    print("Exiting program.")
