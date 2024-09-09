import sys

while True:
    message = sys.stdin.readline().strip()
    print(f"Received: {message}")
    if message == "exit":
        break