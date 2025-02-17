import socket
import sys
import errno
import threading

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

my_username = input("Username: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(True)  # Set to blocking mode to prevent connection issues

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

# Function to receive messages
def receive_messages():
    while True:
        try:
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("\nConnection closed by the server")
                sys.exit()

            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            # Print the received message on a new line without breaking user input
            print(f"\n{username} > {message}")
            print(f"{my_username} > ", end="", flush=True)

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print(f"Reading error: {str(e)}")
                sys.exit()
        except Exception as e:
            print(f"Reading error: {str(e)}")
            sys.exit()

# Start the message receiving thread
receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

# Main loop for sending messages
while True:
    message = input(f"{my_username} > ")
    if message:
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)
