import sysv_ipc

key = sysv_ipc.ftok("/tmp", ord('R'))
memory = sysv_ipc.SharedMemory(key)

while True:
    message = memory.read().decode().strip('\x00')
    print(f"Received: {message}")
    if message == "exit":
        break

memory.detach()
memory.remove()