import socket
import sys

def encode_request(command: str) -> str:
    # 计算总长度（加上前缀后再计算）
    body = command.strip()
    total_len = len(body) + 4  # 3位长度+空格
    return f"{total_len:03d} {body}"

def send_request(host, port, request_line):
    # 转换操作码：PUT -> P, READ -> R, GET -> G
    parts = request_line.strip().split(" ", 1)
    if len(parts) >= 1:
        op = parts[0].upper()
        if op == "PUT":
            request_line = "P " + parts[1] if len(parts) > 1 else "P"
        elif op == "READ":
            request_line = "R " + parts[1] if len(parts) > 1 else "R"
        elif op == "GET":
            request_line = "G " + parts[1] if len(parts) > 1 else "G"
    
    request_msg = encode_request(request_line)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.send(request_msg.encode())

    response = client.recv(1024).decode()
    print(f"Request: {request_line}")
    print(f"Response: {response}\n")

    client.close()

def main():
    if len(sys.argv) < 4:
        print("Usage:")
        print("  python client.py <host> <port> <request>")
        print("  python client.py <host> <port> -f <filename>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    
    if sys.argv[3] == "-f":
        if len(sys.argv) != 5:
            print("Usage: python client.py <host> <port> -f <filename>")
            sys.exit(1)
        filename = sys.argv[4]
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:  # 跳过空行
                        send_request(host, port, line)
        except FileNotFoundError:
            print(f"File not found: {filename}")
            sys.exit(1)
    else:
        request_line = sys.argv[3]
        send_request(host, port, request_line)


if __name__ == "__main__":
    main()
