#/usr/bin/python3

import socket
import traceback
from db_utils import *

class SocketHandler():
    def __init__(self):
        self.host = '127.0.0.1' #back-end server runs locally
        self.port = 4065

        self.sock = socket.socket()

        self.sock.bind((self.host, self.port))

        self.sock.listen(5)

        self.connected_sock, self.clnt_addr = self.sock.accept()

        try:
            while True:
                data = self.connected_sock.recv(4096).decode()

                method = data.split()[0].lower()

                if(method == 'add'):
                    user_id, name = data.split()[1], data.split()[2]
                    print("adding ", user_id, name)
                    add_user(int(user_id), name)
                if(method == 'schedule'):
                    

                    


                print(data)
        except Exception as e:
            self.sock.close()
            traceback.print_exc()



def main():
    sock = SocketHandler()

main()
