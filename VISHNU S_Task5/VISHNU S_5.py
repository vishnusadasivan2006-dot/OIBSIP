# ============================================================
#   Python Real-Time Chat Application (Single File)
#   Created by VISHNU S
#   Internship Project | Oasis Infobyte
# ============================================================

import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 55555

# ─────────────────────────────────────────
#               SERVER SECTION
# ─────────────────────────────────────────

clients = []
nicknames = []

def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                remove_client(client)

def remove_client(client):
    if client in clients:
        index = clients.index(client)
        nickname = nicknames[index]
        clients.remove(client)
        nicknames.remove(nickname)
        client.close()
        broadcast(f"[SERVER] {nickname} has left the chat.".encode('utf-8'))
        print(f"[SERVER] {nickname} disconnected.")

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if message:
                index = clients.index(client)
                nickname = nicknames[index]
                full_message = f"[{nickname}]: {message.decode('utf-8')}"
                print(full_message)
                broadcast(full_message.encode('utf-8'), sender_socket=client)
            else:
                remove_client(client)
                break
        except:
            remove_client(client)
            break

def run_server():
    print("=" * 50)
    print("   Chat Server Started - Created by VISHNU S")
    print("   Oasis Infobyte Internship Project")
    print("=" * 50)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVER] Listening on {HOST}:{PORT}")
    print("[SERVER] Waiting for clients to connect...\n")

    while True:
        client, address = server.accept()
        print(f"[SERVER] New connection from {str(address)}")

        client.send("NICKNAME".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"[SERVER] {nickname} joined the chat.")
        broadcast(f"[SERVER] {nickname} has joined the chat!".encode('utf-8'), sender_socket=client)
        client.send("[SERVER] You are now connected. Start chatting!\n".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.daemon = True
        thread.start()

# ─────────────────────────────────────────
#               CLIENT SECTION
# ─────────────────────────────────────────

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICKNAME':
                pass
            else:
                print(message)
        except:
            print("[ERROR] Connection to server lost.")
            client.close()
            sys.exit()

def send_messages(client):
    while True:
        try:
            message = input("")
            if message.lower() == '/quit':
                print("[INFO] You have left the chat.")
                client.close()
                sys.exit()
            if message.strip():
                client.send(message.encode('utf-8'))
        except:
            print("[ERROR] Failed to send message.")
            client.close()
            sys.exit()

def run_client():
    print("=" * 50)
    print("   Python Chat App - Created by VISHNU S")
    print("   Oasis Infobyte Internship Project")
    print("=" * 50)

    nickname = input("Enter your nickname: ").strip()
    if not nickname:
        nickname = "User"

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("[ERROR] Could not connect to server. Make sure the server is running first!")
        sys.exit()

    # Wait for NICKNAME prompt from server
    msg = client.recv(1024).decode('utf-8')
    if msg == 'NICKNAME':
        client.send(nickname.encode('utf-8'))

    print(f"\n[INFO] Connected to chat server as '{nickname}'")
    print("[INFO] Type your message and press Enter. Type /quit to exit.\n")

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.daemon = True
    receive_thread.start()

    send_messages(client)

# ─────────────────────────────────────────
#               MAIN ENTRY POINT
# ─────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("   Python Chat Application")
    print("   Created by VISHNU S | Oasis Infobyte")
    print("=" * 50)
    print("\nHow do you want to run this?")
    print("  [1] Start as SERVER")
    print("  [2] Start as CLIENT")
    print("  [Q] Quit")

    choice = input("\nEnter your choice (1/2/Q): ").strip().lower()

    if choice == '1':
        run_server()
    elif choice == '2':
        run_client()
    elif choice == 'q':
        print("Goodbye!")
        sys.exit()
    else:
        print("[ERROR] Invalid choice. Please enter 1, 2, or Q.")
        sys.exit()