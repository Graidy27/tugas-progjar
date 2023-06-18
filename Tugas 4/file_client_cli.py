import socket
import json
import base64
import logging

server_address=('172.16.16.101',6666)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    if command_str[-4:] != "\r\n\r\n":
        command_str += "\r\n\r\n"
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        # Look for the response, waiting until socket is done (no more data)
        data_received="" #empty string
        while True:
            #socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
            data = sock.recv(16)
            if data:
                #data is not empty, concat with previous content
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                # no more data, stop the process by break
                break
        # at this point, data_received (string) will contain all data coming from the socket
        # to be able to use the data_received as a dict, need to load it using json.loads()
        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil
    except:
        logging.warning("error during data receiving")
        return False


def remote_list():
    command_str=f"LIST"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str=f"GET {filename}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        #proses file dalam bentuk base64 ke bentuk bytes
        namafile= hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        namafile = "local/" + namafile
        fp = open(namafile,'wb+')
        fp.write(isifile)
        fp.close()
        return True
    else:
        print("Gagal")
        return False
    
def remote_put(strInputCommand=[]):
    filename = "local/" + strInputCommand[1]
    fp = open(f"{filename}",'rb')
    isifile = fp.read()
    command_str=f"PUT {base64.b64encode(isifile).decode()} {strInputCommand[2]}"

    # fp = open(f"{strInputCommand[2]}",'wb+')
    # fp.write(base64.b64decode(isifile))
    # fp.close()
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print(f"[STATUS:SUCCESS] File {filename} berhasil di uploud ke server!")
        return True
    print("Gagal")
    return False
    print(f"Command: {strInputCommand[0]}")
          
def remote_delete(strInputCommand=[]):
    filename = strInputCommand[1]
    command_str=f"DELETE {filename}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print(f"[STATUS:SUCCESS] File {filename} berhasil dihapus dari server!")
        return True
    print("Gagal")
    return False
    

if __name__=='__main__':
    server_address=('172.16.16.101',6666)
    print('Input "exit" to close CLI\n')
    while True:
        strInputCommand = input("Insert your command: ")
        if strInputCommand == "exit":
            print("See you later!\n")
            break
        else:
            strInputCommand = strInputCommand.split()
            if(strInputCommand[0] == "LIST"):
                remote_list()
            elif(strInputCommand[0] == "GET"):
                if(len(strInputCommand) != 2):
                    print("[ERROR] Parameter tidak lengkap")
                    continue
                remote_get(strInputCommand[1])
            elif(strInputCommand[0] == "PUT"):
                if(len(strInputCommand) != 3):
                    print("[ERROR] Parameter tidak lengkap")
                    continue
                remote_put(strInputCommand)
            elif(strInputCommand[0] == "DELETE"):
                if(len(strInputCommand) != 2):
                    print("[ERROR] Parameter tidak lengkap")
                    continue
                remote_delete(strInputCommand)
            else:
                print("[ERROR] Perintah tidak dikenali")
                
            
        # server_address=('172.16.16.101',6666)
        # remote_list()
        # remote_get('donalbebek.jpg')

