import posix_ipc
from ipc_receiver.ipc_receiver import IPCReceiver

class PosixMQReceiver(IPCReceiver):
    def __init__(self, queue_name: str = "/mq"):
        super().__init__()
        self.queue_name = queue_name if queue_name.startswith('/') else f"/{queue_name}"
        try:
            self.mq = posix_ipc.MessageQueue(self.queue_name, posix_ipc.O_CREAT)
        except posix_ipc.ExistentialError:
            print(f"Message queue {self.queue_name} already exists. Connecting to it.")
            self.mq = posix_ipc.MessageQueue(self.queue_name)
        except Exception as e:
            print(f"Error creating/connecting to message queue: {e}")
            self.mq = None

    def receive(self) -> str:
        if not self.mq:
            raise RuntimeError("Message queue is not initialized")
        try:
            message, priority = self.mq.receive()
            decoded_message = message.decode('utf-8').strip()
            self.notify_callbacks(decoded_message)
            return decoded_message
        except posix_ipc.SignalError:
            print("Receive operation interrupted by signal")
            return ""

    def close(self):
        if hasattr(self, 'mq') and self.mq:
            try:
                self.mq.close()
                posix_ipc.unlink_message_queue(self.queue_name)
                print(f"Message queue {self.queue_name} closed and unlinked")
            except posix_ipc.ExistentialError:
                print(f"Message queue {self.queue_name} already unlinked")
            except Exception as e:
                print(f"Error closing message queue: {e}")

    def __del__(self):
        self.close()
