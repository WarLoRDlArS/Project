import sys
import socket
import threading

DFORM = 'utf-8'
FLAG = "\001"
send_thread = []
receive_thread = []

def port_search_bind(server_socket, server_ip):
    """Searches for an empty port and binds the server script to the ip and port"""
    port = 1025
    while port < 66000:
        try:
            server_socket.bind((server_ip, port))
            break
        except:
            port = port + 1

    return port

def Send(client_socket, message):
    message_size = len(str(message).encode(DFORM))
    client_socket.send(str(message_size).encode(DFORM))
    if message_size <= 1024:
        client_socket.send(message.encode(DFORM))
    else:
        for i in range(0, message_size, 1024):
            client_socket.send(message[i:i + 1024].encode(DFORM))

def Receive(client_socket):
    try:
        while True:
            messagesize = int(client_socket.recv(1024).decode(DFORM))
            client_socket.send(FLAG.encode(DFORM))  # Send the flag to indicate readiness for the message
            message = ""
            if messagesize <= 1024:
                message = client_socket.recv(messagesize).decode(DFORM)
            else:
                received_size = 0
                while received_size < messagesize:
                    chunk_size = min(1024, messagesize - received_size)
                    message += client_socket.recv(chunk_size).decode(DFORM)
                    received_size += chunk_size

            print(message)
            # Send an acknowledgment or response if needed
            Send(client_socket=client_socket,message=message)
    except Exception as e:
        print(f"Could not receive anything\nException {e}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_ip = socket.gethostbyname(socket.gethostname())
        server_port = port_search_bind(server_socket, server_ip)

        print(f"Ip Address:{server_ip}\tPort: {server_port}")
        server_socket.listen()
        while True:
            client_socket, client_address = server_socket.accept()

            print(f"Client {client_address} Connected!!")

            thread = threading.Thread(target=Receive, args=(client_socket,))
            receive_thread.append([client_socket, client_address, thread])
            thread.start()

if __name__ == "__main__":
    main()
