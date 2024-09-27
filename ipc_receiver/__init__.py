# ipc_receiver/__init__.py
from .ipc_receiver import IPCHandler
from .socket_receiver import SocketReceiver
from .unix_socket_receiver import UnixSocketReceiver
from .posix_msg_receiver import PosixMQReceiver

# main.py or any other file where you want to use these classes
from ipc_receiver import IPCHandler, SocketReceiver, UnixSocketReceiver, PosixMQReceiver

# Now you can use these classes directly
handler = IPCHandler(SocketReceiver())