import os

FIFO_NAME = "/tmp/myfifo"

if not os.path.exists(FIFO_NAME):
    os.mkfifo(FIFO_NAME)

while True:
    with open(FIFO_NAME, "r") as fifo:
        message = fifo.read()
        print(f"Received: {message.strip()}")
        if "exit" in message.strip():
            break