# 💬 Real-Time Chat Application

A Python application that enables real-time, multi-user chat sessions using a TCP socket server and connected clients.

Created by **[Vishnu S](https://github.com/vishnusadasivan2006)** as part of the **Oasis Infobyte Internship Project (OIBSIP)**.

---

## 🌟 Key Features

- ⚡ **Multi-Client Architecture**: Allows multiple chat clients to connect to a single central server simultaneously.
- 🧵 **Multi-Threaded Execution**: Leverages Python's `threading` module to handle receiving and sending operations concurrently without blocking.
- 📡 **Message Broadcasting**: Forwards messages sent by any client to all other active chat rooms.
- 👤 **Custom Nicknames**: Clients can choose their own handle/nickname upon connecting.
- 🔌 **Graceful Disconnects**: Detects connection dropouts or exits, cleans up client lists, and broadcasts exit notifications to remaining users.
- 🚪 **Simple Navigation Commands**: Users can type `/quit` to log off the server safely.

---

## 🚀 How to Run the App

This application runs as either the central server or a chat participant client, all from a single script.

### Step 1: Start the Chat Server
You must start the server first so clients can connect to it. Run the script and choose option `1`:
```bash
python "VISHNU S_5.py"
```
Select **`1`** to start as server. The server will bind to `127.0.0.1:55555` and wait for incoming connections.

### Step 2: Start One or More Clients
Open another script runner window and execute the same file:
```bash
python "VISHNU S_5.py"
```
Select **`2`** to start as client, input your nickname, and start messaging! You can launch this client multiple times to test chatting between different users.

---

## 💬 Sample Interaction

### Server Log Output:
```text
==================================================
   Chat Server Started - Created by VISHNU S
   Oasis Infobyte Internship Project
==================================================
[SERVER] Listening on 127.0.0.1:55555
[SERVER] Waiting for clients to connect...

[SERVER] New connection from ('127.0.0.1', 58492)
[SERVER] Alice joined the chat.
[SERVER] New connection from ('127.0.0.1', 58510)
[SERVER] Bob joined the chat.
[Alice]: Hello everyone!
[Bob]: Hey Alice, good to see you here!
```

### Client Output (Bob):
```text
==================================================
   Python Chat App - Created by VISHNU S
   Oasis Infobyte Internship Project
==================================================
Enter your nickname: Bob

[INFO] Connected to chat server as 'Bob'
[INFO] Type your message and press Enter. Type /quit to exit.

[SERVER] Alice has joined the chat!
[Alice]: Hello everyone!
Hey Alice, good to see you here!
```

---

## 📂 Folder Structure

```text
├── VISHNU S_Task5/
│   ├── VISHNU S_5.py       # Main Server/Client Chat Application
│   ├── requirements.txt    # Requirements file (standard libraries)
│   └── README.md           # Project documentation (this file)
```
