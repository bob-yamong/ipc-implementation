import os
import socket
from ipc_receiver.ipc_receiver import IPCHandler, IPCReceiver

class UnixSocketReceiver(IPCReceiver):
    def __init__(self, socket_path='/tmp/ipc_socket'):
        super().__init__()
        self.socket_path = socket_path
        if os.path.exists(self.socket_path):
            os.unlink(self.socket_path)
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.bind(self.socket_path)
        self.sock.listen(1)

    def receive(self) -> str:
        conn, addr = self.sock.accept()
        print("Connected by", addr)
        try:
            while True:
                data = conn.recv(1024).decode().strip()
                if not data:
                    print("Client disconnected")
                    break
                
                self.notify_callbacks(data)
        except KeyboardInterrupt:
            print("\nServer stopped by user")
        finally:
            conn.close()
        return data

    def __del__(self):
        self.sock.close()
        if os.path.exists(self.socket_path):
            os.unlink(self.socket_path)
