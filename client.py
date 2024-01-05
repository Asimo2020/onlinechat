import socket
import threading

class ChatClient:
    def __init__(self, server_ip:str, server_port:int):
        self.server_socket_address = (server_ip, server_port)
        self.client_name = ""

    def connect(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect(self.server_socket_address)

    def sending_loop(self):
        while True:
            message = input()
            message_with_name = f"{self.client_name} >> {message}"
            self.server_socket.send(message_with_name.encode())

    def receiving_loop(self):
        while True:
            data = self.server_socket.recv(1024)
            if not data:
                break
            decoded_data = data.decode()
            if self.client_name in decoded_data:
                formatted_data = decoded_data.replace(self.client_name, "Me")
            else:
                formatted_data = decoded_data
            print(formatted_data)

    def start(self):
        self.connect()
        self.client_name = input("Enter your name: ")
        self.server_socket.send(self.client_name.encode())
        sending_loop = threading.Thread(target=self.sending_loop)
        sending_loop.start()
        self.receiving_loop()

client = ChatClient("127.0.0.1", 54321)
client.start()