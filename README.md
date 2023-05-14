# Simple UDP File Transfer Tool

Transfer files from server to client using the UDP protocol with the following features:

1. Split data into chunks of 512 bytes.
2. Pack the chunk with its order, its sha1 hash, and some metadata into a packet.\
   (As UDP does not have robust packet delivery or sequencing)
4. Send the packet to the client using UDP.
5. The client collect the packet, send an ACK, and build the file back.

This is only a very very simple tool for demonstration purposes, written in less than 30 minutes.

## Commands

* "get-file-list":\
The server returns available file list as "Files: {filename1} {filename2} {filename3} ..."
* "get-file {filename1} {filename2} {filename3}":\
Downloads the requested files. Can accept multiple files in a single command.

## Deployment

Server:

```sh
python server.py {PORT}
```

Client:

```sh
python client.py {SERVER_IP} {SERVER_PORT}
```
