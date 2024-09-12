# Shared Memory
## 사용방법
```bash
gcc ipc_sender.c -o sender
sudo ./sender

# 다른 터미널
pip install sysv-ipc
sudo python3 ipc_receiver.py
```

## 결과
![](./img/image.png)