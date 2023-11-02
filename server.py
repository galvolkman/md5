import socket
from threading import Thread
import hashlib
import random


class Server:
    def __init__(self):
        self.server_socket = socket.socket()
        self.server_socket.bind(("0.0.0.0", 8800))
        self.server_socket.listen()
        self.clients = []
        self.threads = []
        self.secret = random.randint(1000000000, 9999999999)
        self.ans = hashlib.md5(str(self.secret).encode()).hexdigest()

    def handle_server(self):
        for i in range(10):
            try:
                (client_socket, client_address) = self.server_socket.accept()
            except socket.error:
                break
            print("Client connected")
            self.clients.append(client_socket)
            self.threads.append(Thread(target=self.handle_client, args=(client_socket, i, )).start())

    def handle_client(self, client_socket, index):
        print("here")
        bottom = 1000000 + index * 1000000
        top = 1000000 + (index + 1) * 1000000
        ans_range = f"{bottom} {top} {self.ans}"
        client_socket.send(ans_range.encode())
        data = client_socket.recv(1024).decode()
        while len(data) == 0:
            data = client_socket.recv(1024).decode()
            pass
        if data == "no":
            client_socket.close()

        else:
            print(f"the original num is: {data}")
            client_socket.close()
            self.server_socket.close()

    def stop_clients(self, og_num):

        for client in self.clients:
            client.close()
        print(f"the original num is: {og_num}")
        self.server_socket.close()


if __name__ == '__main__':
    ser = Server()
    ser.handle_server()