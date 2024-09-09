import posix_ipc
import time

# Open the message queue
mq = posix_ipc.MessageQueue("/mq", posix_ipc.O_CREAT)

try:
    while True:
        # Receive message
        message, priority = mq.receive()
        # Decode the message (assuming UTF-8 encoding)
        decoded_message = message.decode('utf-8').strip()
        print(f"Received: {decoded_message}")
        
        if 'exit' in decoded_message.lower():
            break

        # Small delay to prevent busy-waiting
        time.sleep(0.1)

finally:
    # Close and unlink the message queue
    mq.close()
    try:
        posix_ipc.unlink_message_queue("/test_mq")
    except posix_ipc.ExistentialError:
        pass