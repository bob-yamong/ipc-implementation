> [!NOTE]
> 버퍼 이용해서 실시간성이 조금 떨어지는 것 같음

플러시 이용해서 강제로 전송후 던지는 방법이 필요한 듯

## 그냥 사용하는 경우
### 사용방법
```bash
gcc ipc_sender.c -o sender
sudo ./sender

# 다른 터미널
sudo python3 ipc_receiver.py
```

### 결과
![common](img/common_image.png)

## flush를 이용해서 즉시 비우는 경우
### 사용방법
```bash
gcc flush_ipc_sender.c -o sender
sudo ./sender

# 다른 터미널
sudo python3 flush_ipc_receiver.py
```

### 결과
![flush](img/flush_image.png)