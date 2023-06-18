from socket import *
import socket
import threading
import logging
from time import sleep
import sys
from datetime import datetime
# import win32file
# win32file._setmaxstdio(2048)


class ProcessTheClient(threading.Thread):
    def __init__(self,connection,address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self, daemon=True)

    def run(self):
        while True:
            data = self.connection.recv(32)
            if data:
                if data.startswith(b"TIME") and data.endswith(b"\r\n"):
                    waktuSekarang = datetime.now()
                    # print(waktuSekarang)
                    
                    formatWaktu = waktuSekarang.strftime("%H:%M:%S")
                    # print(formatWaktu)
                    
                    response = f'JAM {formatWaktu}\r\n'
                    # print(f'[DATA SEND TO CLIENT] {response}')
                    
                    response = bytes(response, 'utf-8')
                    
                    self.connection.sendall(response)
            else:
                break
        sleep(100)
        self.connection.close()

class Server(threading.Thread):
    print("[STATUS] Server is running")
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('0.0.0.0',45000))
        self.my_socket.listen(1)
        threads = 0     #thread counter
        while True:
            self.connection, self.client_address = self.my_socket.accept()
            logging.warning(f"connection from {self.client_address}")
            
            try:
                clt = ProcessTheClient(self.connection, self.client_address)
                print("{} server threads created.\n".format(threads))
                threads += 1
                clt.start()
                self.the_clients.append(clt)
            except RuntimeError:    #too many throws a RuntimeError
                break
        # print("{} server threads created.\n".format(threads))

def main():
    svr = Server()
    svr.start()

if __name__=="__main__":
    main()