import socket
import threading

def handle_client(client_socket, address):
    print(f"[+] Connected with {address}")
    
    try:
        data = client_socket.recv(1024).decode()
        if not data:
            return

        print(f"[REQ] {data.strip()}")

        # 解析协议内容
        size_str = data[:3]
        message = data[4:]
        parts = message.strip().split(" ", 2)

        if len(parts) < 2:
            response = "ERR invalid message format"
        else:
            op, key = parts[0], parts[1]
            value = parts[2] if len(parts) == 3 else ""
            
            if op == 'P':
                response = f"OK ({key}, {value}) added"  # 先假装添加成功
            elif op == 'R':
                response = f"OK ({key}, dummy_value) read"
            elif op == 'G':
                response = f"OK ({key}, dummy_value) removed"
            else:
                response = "ERR unknown operation"

        # 加上响应协议格式
        full_response = f"{len(response)+4:03d} {response}"
        client_socket.send(full_response.encode())

    except Exception as e:
        print(f"[ERR] {e}")
    
    client_socket.close()

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", port))
    server.listen(5)
    print(f"[SERVER] Listening on port {port}...")

    while True:
        client_socket, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_server(port)
