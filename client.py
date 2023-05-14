import socket
import hashlib
import pickle
import sys

chunk_size = 512  # bytes
if len(sys.argv) != 3:
    print("usage error")
    exit(1)
ip = sys.argv[1]
port = int(sys.argv[2])
server_address =(ip,port)


def recv_list(sock):
    pkt_b, _ = sock.recvfrom(4096)
    try:
        pkt = pickle.loads(pkt_b)
    except :
        sock.sendto(b"get-file-list",server_address)
    hash_local = hashlib.sha1(pkt["payload"]).hexdigest()
    if pkt["hash"] == hash_local:
        sock.sendto(b"ACK",server_address)
        dir = pkt["payload"].decode()
        print("Files: {}".format(dir))



def recv(sock):
    pkt_list = []
    while True:
        pkt_b, client_address = sock.recvfrom(4096)
        try:
            pkt = pickle.loads(pkt_b)
        except:
            # print("decode error")
            continue
        hash_server = hashlib.sha1(pkt["payload"]).hexdigest()
        if (pkt["hash"] == hash_server):
            sock.sendto(b"ack", client_address)
            pkt_list.append(pkt)
            if pkt["size"] < chunk_size and not pkt["is_filename"]:
                break


    filename = pkt_list[0]["payload"]
    with open(filename, "wb") as FILE:
        for p in pkt_list[1:]:
            FILE.write(p["payload"])

    # print("revieved {} from {}".format(filename, client_address))


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        cmd = input("% ")
        cmd_list = cmd.split()
        if cmd_list[0] == "get-file-list":
            sock.sendto(b"get-file-list",server_address)
            # print("getting file")
            recv_list(sock)
        elif cmd_list[0] == "get-file":
            sock.sendto(cmd.encode(),server_address)
            for i in range(len(cmd_list) - 1):
                recv(sock)
        elif cmd_list[0] == "exit":
            break