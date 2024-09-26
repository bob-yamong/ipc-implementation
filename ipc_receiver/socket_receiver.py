import socket
import os
import sys
from ipc_receiver.ipc_receiver import IPCHandler, IPCReceiver 

class SocketReceiver(IPCReceiver):
    def __init__(self, host='localhost', port=12345):
        super().__init__()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)

    def receive(self) -> None:
        print(f"Waiting for connection on {self.host}:{self.port}...")
        conn, addr = self.sock.accept()
        print(f"Connected by {addr}")
        try:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                self.notify_callbacks(data)
                if data.strip().lower() == 'exit':
                    break
        finally:
            conn.close()
            print("Connection closed")