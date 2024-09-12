import socket
import os

SOCKET_NAME = "/tmp/ipc_socket"

if os.path.exists(SOCKET_NAME):
    os.unlink(SOCKET_NAME)

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.bind(SOCKET_NAME)
sock.listen(1)

conn, addr = sock.accept()
print("Connected")

while True:
    data = conn.recv(256).decode()
    if not data:
        break
    print(f"Received: {data.strip()}")
    if data.strip() == "exit":
        break

conn.close()
sock.close()
os.unlink(SOCKET_NAME)