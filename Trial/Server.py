import socket
import threading

DFORM = 'utf-8'
FLAG = "\001"
connected_clients = []
receive_threads = []  # Rename the list to avoid conflicts
send_threads = []  # Rename the list to avoid conflicts

def port_search_bind(server_socket, server_ip):
    port = 1025
    while port < 66000:
        try:
            server_socket.bind((server_ip, port))
            break
        except:
            port = port + 1

    return port

def message_input():
    message = input("Enter Message :")
    return message

def Send(client_socket, client_address):
    while True:
        message = message_input()
        try:
            message_size = len(str(message).encode(DFORM))
            client_socket.send(str(message_size).encode(DFORM))
            confirmation_flag = client_socket.recv(1024).decode(DFORM)
            if confirmation_flag == FLAG:
                if message_size <= 1024:
                    client_socket.send(message.encode(DFORM))
                else:
                    for i in range(0, message_size, 1024):
                        client_socket.send(message[i:i + 1024].encode(DFORM))
        except Exception as e:
            print("Couldn't Send Message: " + str(message))
            print(f"Exception {e}")
            break

def Receive(client_socket, client_address):
    try:
        while True:
            messagesize = int(client_socket.recv(1024).decode(DFORM))
            client_socket.send(FLAG.encode(DFORM))
            message = ""
            if messagesize <= 1024:
                message = client_socket.recv(messagesize).decode(DFORM)
            else:
                received_size = 0
                while received_size < messagesize:
                    chunk_size = min(1024, messagesize - received_size)
                    message += client_socket.recv(chunk_size).decode(DFORM)
                    received_size += chunk_size

            if message.lower() == '\exit':
                print(f"Client {client_address} requested disconnection.")

                # Send a confirmation flag to acknowledge the client's disconnection request
                client_socket.send(FLAG.encode(DFORM))

                # Stop the receive and send threads
                for thread in receive_threads:
                    if thread[0] == client_socket:
                        thread[1].join()
                        receive_threads.remove(thread)
                        break
                for thread in send_threads:
                    if thread[0] == client_socket:
                        thread[1].join()
                        send_threads.remove(thread)
                        break

                # Remove the client from the list
                connected_clients.remove((client_socket, client_address))
                break

            print(message)
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

            # Add the client to the list
            connected_clients.append((client_socket, client_address))

            # Start separate threads for sending and receiving
            receive_thread = threading.Thread(target=Receive, args=(client_socket, client_address))
            send_thread = threading.Thread(target=Send, args=(client_socket, client_address))

            # Append the threads to the corresponding lists
            receive_threads.append((client_socket, receive_thread))
            send_threads.append((client_socket, send_thread))

            receive_thread.start()
            send_thread.start()

if __name__ == "__main__":
    main()