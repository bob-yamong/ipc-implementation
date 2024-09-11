import mmap
import os

FILE_NAME = "/tmp/mmaptest"
MSG_SIZE = 256

with open(FILE_NAME, "r+b") as f:
    mm = mmap.mmap(f.fileno(), MSG_SIZE)
    
    while True:
        mm.seek(0)
        message = mm.read(MSG_SIZE).decode().strip('\x00')
        print(f"Received: {message}")
        if "exit" in message :
            break

    mm.close()