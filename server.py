#!/usr/bin/python3
import socket
import sys
import os
import pickle
import hashlib


chunk_size = 512


def make_pkt(data, SN,  bool=False):
    seq = SN
    SN += 1
    size = len(data)
    payload = data
    hash = hashlib.sha1(data).hexdigest()
    is_filename = bool
    return pickle.dumps(
        {
            "SN": seq,
            "size": size,
            "payload": payload,
            "hash": hash,
            "is_filename": is_filename
        }
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage error")
        exit(1)
    ip = "0.0.0.0"
    port = int(sys.argv[1])

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (ip, port)
    sock.bind(server_address)
    while True:
        sock.settimeout(None)
        data,address = sock.recvfrom(4096)
        sock.settimeout(0.1)
        if not data:
            continue
        msg = data.decode()
        msg = msg.split()

        if msg[0] == "get-file-list":
            file_list = os.listdir()
            dir = ""
            for filename in file_list:
                dir = dir + filename + " "
            data = make_pkt(dir.encode() , 0)
            sock.sendto(data, address)
            try:
                    _,_ = sock.recvfrom(1024) # get ack
            except KeyboardInterrupt:
                print("fxxk_2020!")
                exit(1)
            except:                        
                print("resending ")
                continue
        
        elif msg[0] == "get-file":
            for filename in msg[1:]:
                # make
                SN = 0
                pkt_list = []
                pkt_list.append(make_pkt(filename.encode(),SN, True))
                SN += 1
                FILE = open(filename, "rb")
                data = FILE.read(chunk_size)
                while data:
                    pkt_list.append(make_pkt(data,SN))
                    data = FILE.read(chunk_size)
                    SN += 1
                FILE.close()
                if len(pkt_list) == 1 or len(pkt_list) == 0 or len(pkt_list[-1]) == chunk_size:
                    pkt_list.append(make_pkt(b""))

                # send
                x = 0
                while x < len(pkt_list):
                    sock.sendto(pkt_list[x],address)
                    try:
                        _,_ = sock.recvfrom(1024) # get ack
                        x += 1
                    except KeyboardInterrupt:
                        print("fxxk_2020!")
                        exit(1)
                    except:
                        print("resending {}".format(x))
                        continue



# def get_file_list_handler(sock):
#     dir =bytes( os.listdir())
#     hash = hashlib.sha1(dir).hexdigest()    
#     pkt = pickle.dumps(
#         {
#             "list": dir
#             "hash":hash
#         }
#     )



# def parse(msg):
#     cmd = msg.split()
#     if cmd[0] == "get-file-list":
#         return (cmd , "get-file-list")
#     elif cmd[0] == "get-file":
#         return (cmd,"get-file")
#     else:
#         return (None, None)

# if __name__ == "__main__":
#     cmd = []
#     if len(sys.argv) != 2:
#         print("usage error")
#         exit(1)

#     # Create a UDP socket
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#     port = int (sys.argv[1])

#     # Bind the socket to the port
#     server_address = ('0.0.0.0', port)
#     #print('starting up on {} port {}'.format(*server_address))
#     sock.bind(server_address)

#     while True:
#         #print('\nwaiting to receive message')
#         data, address = sock.recvfrom(4096)
#         if data:
#             cmd , which= parse(data.decode())
#             if cmd:
#                 if which == "get-file-list":
#                     get_file_list_handler(sock)
#                 elif which == "get-file":
#                     get_file_handler(cmd, sock)
