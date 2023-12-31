import socket
import threading
import sys
import time

FLAG = "\001"
DFORM="utf-8" 
thread_list = []
conditionStatus={"exit":False,}

def message_input(ClientConn):
    message = input("Enter Message :")
    if message == "\exit": 
        # for i in thread_list:
        #     i.join()
        # ClientConn.close()
        conditionStatus["exit"]=True
        print("Program Closing!!")
        sys.exit()   
    else :
        return message   

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
        message = message_input(ClientConn)
        if message.lower() == 'exit':
            break
        try:
            message_size = len(str(message).encode(DFORM))
            ClientConn.send(str(message_size).encode(DFORM))
            confirmation_flag = ClientConn.recv(1024).decode(DFORM)  # Receive the flag from the server
            if confirmation_flag == FLAG:
                if message_size <= 1024:
                    ClientConn.send(message.encode(DFORM))
                else:
                    for i in range(0, message_size, 1024):
                        ClientConn.send(message[i:i + 1024].encode(DFORM))
        except Exception as e:
            print("Couldn't Send Message: " + str(message))
            print(f"Exception {e}")
            break
        time.sleep(1)

def recMessage(clientSock):
    while True:
        try:
            messagesize = int(clientSock.recv(1024).decode(DFORM))
            message = ""
            if messagesize <= 1024:
                message = clientSock.recv(messagesize).decode(DFORM)
            else:
                received_size = 0
                while received_size < messagesize:
                    chunk_size = min(1024, messagesize - received_size)
                    message += clientSock.recv(chunk_size).decode(DFORM)
                    received_size += chunk_size

            print(message)
        except Exception as e:
            print(f"Error in receiving message: {str(e)}")
            break


def checkCondition(clientConn):
    """
    This function is used to check for various conditions like exit program,etc
    """
    while True:
        if conditionStatus["exit"]:
            for thread in thread_list:
                thread.join()
            clientConn.close()
            break

def main():
    print("Enter Server IP:")
    serverIP = input()
    print("Enter Server Port:")
    serverPort = int(input())
    clientconn = ClientConnect(serverIP, serverPort)

    try:
        send = threading.Thread(target=sendMessage, args=(clientconn,),daemon=True)
        thread_list.append(send)
        recv = threading.Thread(target=recMessage, args=(clientconn,),daemon=True)
        thread_list.append(recv)
        send.start()
        recv.start()
        send.join()  # Wait for send thread to finish
        clientconn.close()  # Close the socket after sending is done
        recv.join()  # Wait for receive thread to finish

    except Exception as e:
        print("Error:", str(e))
        print("Couldn't create threads")

    print("Exiting program.")

    checkCondition(clientconn)


if __name__ == "__main__":
    main() 