import sys
import socket
import threading

DFORM = 'utf-8'
send_thread = []
receive_thread = []
def port_search_bind(server_socket,server_ip):
    """Searches for an empty port and binds the server script to the ip and port"""
    port = 1025
    while port < 66000:
        try:
            server_socket.bind((server_ip,server_port))
            break
        except :
            port = port+1

    return port

def Send(client_socket,message):
     message_size = len(str(message).encode(DFORM))
     client_socket.send(str(message_size).encode(DFORM))
     if message_size <= 1024:
         client_socket.send(message.encode(DFORM))
     else:
         for i in range(0,message_size,1024):
             client_socket.send(message.encode(DFORM))

def Receive(client_socket):
    try:
        while True: 
            messagesize = int(client_socket.recv(1024).decode(DFORM))
            message = ""
            if messagesize <= 1024:
                message = client_socket.recv(messagesize).decode(DFORM)
            else :
                for i in range(0,messagesize,1024):
                    message += client_socket.recv(i).decode(DFORM)
            print(message)
            Send(client_socket, message)
    except Exception as e:
        print(f"Couldnt receive anything\nException {e}")

def main():
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server_socket:
        server_ip = socket.gethostbyname(socket.gethostname())
        server_port = port_search_bind(server_socket,server_ip)

        print(f"Ip Address:{server_ip}\tPort: {server_port}")
        server_socket.listen()
        while True:
            client_socket,client_address = server_socket.accept()

            print(f"Client {client_address} Connected!!")

            thread = threading.Thread(target = Receive, args = (client_socket,))
            receive_thread.append([client_socket,client_address,thread])
            thread.start()

if __name__ == "__main__":
    main()