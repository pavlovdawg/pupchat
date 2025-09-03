import socket
import threading
import sys

BLUE = "\033[94m"
RESET = "\033[0m"
GREEN = "\033[92m"
WHITE = "\033[97m"
RED = "\033[91m"
YELLOW = "\033[33m"

HOST = '127.0.0.1'
PORT = 12345

def receive_messages(conn, username):
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            sys.stdout.write('\r')           
            sys.stdout.flush()
            
            print(f"\n{RED}{username}: {WHITE}{data}{RESET}")

            sys.stdout.write(f"{BLUE}You: {RESET}")
            sys.stdout.flush()

        except:
            break

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)  

print(f"{YELLOW}Server listening on {HOST}:{PORT}...{RESET}")

conn, addr = server_socket.accept()
username = conn.recv(1024).decode()

print(f"{GREEN}{username} joined the pack from {addr}{RESET}")
threading.Thread(target=receive_messages, args=(conn, username), daemon=True).start()

while True:
    try:
        message = input(f"{BLUE}You: {RESET}")
        if message.lower() == "/quit":
            break
        formatted = f"{RED}Server: {WHITE}{message}{RESET}"
        conn.send(formatted.encode())
    except KeyboardInterrupt:
        break

conn.close()
