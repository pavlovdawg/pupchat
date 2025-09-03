import socket
import threading
import sys

BLUE = "\033[94m"
GREEN = "\033[92m"
WHITE = "\033[97m"
RED = "\033[91m"
RESET = "\033[0m"

HOST = '127.0.0.1'
PORT = 12345

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break

            sys.stdout.write('\r')
            sys.stdout.flush()

            print(f"\n{data}")

            sys.stdout.write(f"{BLUE}You: {RESET}")
            sys.stdout.flush()

        except:
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

username = input(f"{WHITE}Enter your username: {RESET}")
client_socket.send(username.encode())

print(f"{GREEN}Connected to server at {HOST}:{PORT}{RESET}")

recv_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
recv_thread.start()

while True:
    try:
        message = input(f"{BLUE}You: {RESET}")
        if message.lower() == "/quit":
            break
        client_socket.send(message.encode())
    except KeyboardInterrupt:
        break

client_socket.close()
