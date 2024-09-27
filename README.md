# ipc-implementation
Some IPC implementations

## Test
```bash
apt install python3.10-venv
python3 -m venv .ipc
source .ipc/bin/activate

pip install -r requirements.txt
```

## Example
```py
from ipc_receiver import IPCHandler, SocketReceiver, UnixSocketReceiver, PosixMQReceiver

def main():
    receiver = PosixMQReceiver()
    handler = IPCHandler(receiver)

    receiver.add_callback(lambda message: print(f"Received: {message}"))
    handler.receive_forever()

if __name__ == "__main__":
    main()
```