import socket
import hashlib
from threading import Thread
import time

class Worker:
    def __init__(self, bottom, top, secret):
        self.found = False
        self.done = False
        self.founded_secret = None
        self.bottom = bottom
        self.top = top
        self.secret = secret

    def handle_thread(self):
        for i in range(self.bottom, self.top):
            if hashlib.md5(str(i).encode()).hexdigest() == self.secret:
                print(f"the num is: {i}")
                self.founded_secret = i
                #.my_socket.send(str(i).encode())
                self.found = True
                break

        self.done = True

class Client:
    def __init__(self):
        self.my_socket = socket.socket()
        self.my_socket.connect(("127.0.0.1", 8800))
        self.ans_range = self.my_socket.recv(1024).decode().split(" ")
        self.bottom = int(self.ans_range[0])
        self.top = int(self.ans_range[1])
        self.result = self.ans_range[2]
        self.found = False
        self.num_range = self.top - self.bottom
        print(f"{self.bottom} \n{self.top}")
        self.dif = self.num_range/10

    def create_threads(self):
        workers = []
        threads = []
        for i in range(10):
            bottom1 = int(self.bottom + (i * self.dif))
            top1 = int(self.bottom + ((i + 1) * self.dif))
            print(f"{bottom1} \n{top1}")
            worker = Worker(bottom1, top1, self.result)
            workers.append(worker)
            t = Thread(target=worker.handle_thread)
            t.start()
            threads.append(t)

        found = False
        while not found:
            time.sleep(10)
            count = 0
            for i in range(len(threads)):
                if not threads[i].is_alive():
                    count += 1
                    if workers[i].found:
                        found = True
                        self.my_socket.send(str(workers[i].founded_secret).encode())

            if count == len(threads):
                self.my_socket.send("no".encode())
                break



    def handle_thread(self, bottom, top, result):
        for i in range(bottom, top):
            if hashlib.md5(str(i).encode()).hexdigest() == result:
                print(f"the num is: {i}")
                self.my_socket.send(str(i).encode())
                self.found = True
                break

        if not self.found:
            self.my_socket.send("no".encode())

        self.my_socket.close()


if __name__ == '__main__':
    cli = Client()
    cli.create_threads()