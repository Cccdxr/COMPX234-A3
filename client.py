import socket
import sys

def encode_request(command: str) -> str:
    # 计算总长度（加上前缀后再计算）
    body = command.strip()
    total_len = len(body) + 4  # 3位长度+空格
    return f"{total_len:03d} {body}"

def main():
    if len(sys.argv) != 4:
        print("Usage: python client.py <host> <port> <request>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    request = sys.argv[3]

    # 协议封装
    request_msg = encode_request(request)
   
    # 发送请求
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.send(request_msg.encode())
    
    # 接收并打印响应
    response = client.recv(1024).decode()
    print(f"Response: {response}")
    
    
    client.close()

if __name__ == "__main__":
    main()
