
import socket
import threading

class ChatServer:
    def __init__(self, ip:str, port:int):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((ip, port))
        self.server_socket.listen()
        self.clients = {}

    def accept(self):
        conn, addr = self.server_socket.accept()
        print(f"client {addr} is connected")
        return conn

    def clientHandler(self, conn:socket, client_name:str):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = f"{client_name} >> {data.decode()}"
            print(message)
            self.broadcast(message, conn)

    def broadcast(self, message:str, sender_conn:socket) -> None:
        for client, conn in self.clients.items():
            if conn != sender_conn:
                conn.send(message.encode())

    def start(self) -> None:
        while True:
            client = self.accept()
            client_name = client.recv(1024).decode()
            self.clients[client_name] = client
            clientHandlerThread = threading.Thread(target=self.clientHandler, args=(client, client_name))
            clientHandlerThread.start()

server = ChatServer("127.0.0.1", 54321)
server.start()