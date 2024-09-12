import sysv_ipc

key = sysv_ipc.ftok("/tmp", ord('R'))
memory = sysv_ipc.SharedMemory(key)
semaphore = sysv_ipc.Semaphore(key)

while True:
    semaphore.acquire()
    message = memory.read().decode().strip('\x00')
    semaphore.release()
    
    print(f"Received: {message}")
    if message == "exit":
        break

memory.detach()
memory.remove()
semaphore.remove()