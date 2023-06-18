import sys
import socket
import logging
import threading
import ctypes
from time import sleep
flag = 0
def kirim_data():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # logging.warning("membuka socket")

    server_address = ('172.16.16.101', 45000)
    try:
        # logging.warning(f"opening socket {server_address}")
        sock.connect(server_address)
    except ConnectionRefusedError:
        global flag 
        flag = 1
        return
    try:
        # Send data
        message = 'TIME \r\n'
        # logging.warning(f"[CLIENT] sending {message}")
        sock.sendall(message.encode())
        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            # print("{} threads created.\n".format(threads))
            try:
                data = sock.recv(16)
                amount_received += len(data)
                # logging.warning(f"[DITERIMA DARI SERVER] {data}")
            except ConnectionResetError:
                return
    finally:
        # logging.warning("closing")
        sock.close()
    sleep(100)
    return

def main():
    threads = 0     #thread counter
    y = 30000     #a MILLION of 'em!
    for i in range(y):
        try:
            global flag 
            if(flag == 1):
                print("Server closed")
                break
            x = threading.Thread(target=kirim_data)
            threads += 1    #thread counter
            x.start()       #start each thread
            print(f'current thread: {threads}')
        except RuntimeError:    #too many throws a RuntimeError
            break
    print("{} threads created.\n".format(threads))

if __name__ == "__main__":
    main()
