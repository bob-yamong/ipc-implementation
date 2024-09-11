import os
import select
import fcntl

FIFO_NAME = "/tmp/myfifo"

def non_blocking_read(fd):
    try:
        return os.read(fd, 256).decode().strip()
    except BlockingIOError:
        return None

if not os.path.exists(FIFO_NAME):
    os.mkfifo(FIFO_NAME)

print(f"Opening FIFO: {FIFO_NAME}")
fd = os.open(FIFO_NAME, os.O_RDONLY | os.O_NONBLOCK)

# Set up polling
poll = select.poll()
poll.register(fd, select.POLLIN)

try:
    while True:
        events = poll.poll(1000)  # Wait for up to 1 second
        if events:
            message = non_blocking_read(fd)
            if message:
                print(f"Received: {message}")
                if message == "exit":
                    break
        else:
            print("Waiting for data...")
finally:
    os.close(fd)
    os.unlink(FIFO_NAME)