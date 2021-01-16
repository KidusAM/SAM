#/usr/bin/python3

import socket

class SocketHandler():
    def __init__(self):
        self.host = '127.0.0.1' #back-end server runs locally
        self.port = 4065

        self.sock = socket.socket()

        self.sock.bind((self.host, self.port))

        self.sock.listen(5)

        self.connected_sock, self.clnt_addr = self.sock.accept()

        while True:
            data = self.connected_sock.recv(1024).decode()
            print(data)


def main():
    sock = SocketHandler()

main()
