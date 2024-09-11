import signal
import os
import sys

# Use SIGUSR1 and SIGUSR2 for communication
SIGUSR1 = signal.SIGUSR1
SIGUSR2 = signal.SIGUSR2

received_bits = []
current_message = []

def signal_handler(signum, frame):
    global received_bits, current_message
    if signum == SIGUSR1:
        received_bits.append(0)
    elif signum == SIGUSR2:
        received_bits.append(1)
    
    if len(received_bits) == 8:
        char = chr(int(''.join(map(str, received_bits)), 2))
        received_bits = []
        
        if char == '\n':
            # Message is complete, process it
            message = ''.join(current_message)
            print(f"\nReceived message: {message}")
            
            if "exit" in message:
                print("Received exit command. Terminating...")
                sys.exit(0)
            
            current_message = []
            print("Waiting for next message...")
        else:
            current_message.append(char)
            print(char, end='', flush=True)

def main():
    print(f"Python receiver process started. PID: {os.getpid()}")
    print("Waiting for signals...")

    signal.signal(SIGUSR1, signal_handler)
    signal.signal(SIGUSR2, signal_handler)

    while True:
        signal.pause()

if __name__ == "__main__":
    main()