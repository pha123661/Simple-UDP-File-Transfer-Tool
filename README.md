# Simple UDP File Transfer Tool

Transfer files from server to client using the UDP protocal.

A very very simple tool for demonstration purposes, written in less than 30 minutes.

## Commands

* "get-file-list":\
The server returns available file list as "Files: {filename1} {filename2} {filename3} ..."
* "get-file {filename1} {filename2} {filename3}":\
Downloads the requested files. Can accept multiple files in a single command.

Note: The server splits the file into 1024 byte blocks, and handles the order of UDP transfer.

## Deployment

Server:

```sh
python server.py {PORT}
```

Client:

```sh
python client.py {SERVER_IP} {SERVER_PORT}
```
