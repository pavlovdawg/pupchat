import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

HOST = '127.0.0.1'
PORT = 12345

# --- Networking ---
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

username = input("Enter your username: ")
client_socket.send(username.encode())

# --- GUI Setup ---
root = tk.Tk()
root.title(f"PupChat - {username}")

chat_area = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, state='disabled', width=50, height=20
)
chat_area.pack(padx=10, pady=10)

entry = tk.Entry(root, width=40)
entry.pack(side=tk.LEFT, padx=10, pady=10)

send_btn = tk.Button(root, text="Send")
send_btn.pack(side=tk.LEFT, padx=5)

# --- Placeholder behavior ---
placeholder = "Send message..."

def set_placeholder():
    entry.delete(0, tk.END)
    entry.insert(0, placeholder)
    entry.config(fg="gray")

def clear_placeholder(event=None):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)
        entry.config(fg="black")

def restore_placeholder(event=None):
    if entry.get() == "":
        set_placeholder()

def on_keypress(event):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)
        entry.config(fg="black")

# initialize placeholder on startup
set_placeholder()

entry.bind("<FocusIn>", clear_placeholder)
entry.bind("<FocusOut>", restore_placeholder)
entry.bind("<Key>", on_keypress)  # NEW: clear on typing

# --- Send message ---
def send_message(event=None):
    text = entry.get()
    if text and text != placeholder:
        client_socket.send(text.encode())
        entry.delete(0, tk.END)
    restore_placeholder()  # reapply placeholder if empty

send_btn.config(command=send_message)
entry.bind("<Return>", send_message)

# --- Message Receiver Thread ---
def receive_messages():
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            chat_area.config(state='normal')
            chat_area.insert(tk.END, data + "\n")
            chat_area.config(state='disabled')
            chat_area.yview(tk.END)  # auto scroll
        except:
            break

threading.Thread(target=receive_messages, daemon=True).start()

# --- Connection message ---
chat_area.config(state='normal')
chat_area.insert(tk.END, f"✅ Connected as {username}\n")
chat_area.config(state='disabled')
chat_area.yview(tk.END)

# --- Run GUI ---
root.mainloop()
client_socket.close()
