import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 12345

def handle_client(conn, addr):
    username = conn.recv(1024).decode()
    print(f"{username} joined from {addr}")

    def receive_messages():
        while True:
            try:
                data = conn.recv(1024).decode()
                if not data:
                    break
                # print client message
                print(f"\n{username}: {data}")
                # re-draw server operator prompt
                sys.stdout.write("You: ")
                sys.stdout.flush()
                # echo back to client
                conn.send(f"{username}: {data}".encode())
            except:
                break

    threading.Thread(target=receive_messages, daemon=True).start()

    # server operator chat loop
    while True:
        try:
            message = input("You: ")
            if message.lower() == "/quit":
                break
            formatted = f"Server: {message}"
            conn.send(formatted.encode())
        except KeyboardInterrupt:
            break

    conn.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"Server listening on {HOST}:{PORT}...")

    conn, addr = server_socket.accept()
    handle_client(conn, addr)


if __name__ == "__main__":
    main()
