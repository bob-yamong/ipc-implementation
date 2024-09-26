from abc import ABC, abstractmethod
from typing import Callable, List

class IPCReceiver(ABC):
    def __init__(self):
        self.callbacks: List[Callable[[str], None]] = []

    @abstractmethod
    def receive(self) -> str:
        pass

    def add_callback(self, callback: Callable[[str], None]):
        self.callbacks.append(callback)

    def remove_callback(self, callback: Callable[[str], None]):
        self.callbacks.remove(callback)

    def notify_callbacks(self, message: str):
        for callback in self.callbacks:
            callback(message)


class IPCHandler:
    def __init__(self, ipc_receiver: IPCReceiver):
        self.receiver = ipc_receiver

    def receive_data(self) -> str:
        return self.receiver.receive()

    def receive_forever(self):
        try:
            while True:
                self.receive_data()
        except KeyboardInterrupt:
            print("\nServer stopped by user")

    def add_callback(self, callback: Callable[[str], None]):
        self.receiver.add_callback(callback)

    def remove_callback(self, callback: Callable[[str], None]):
        self.receiver.remove_callback(callback)