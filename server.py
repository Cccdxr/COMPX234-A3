import socket
import threading
import time  

tuple_space = {}  # 共享元组空间
lock = threading.Lock()  # 用于线程同步

# 新增统计变量
total_clients = 0
total_ops = 0
put_count = 0
get_count = 0
read_count = 0
err_count = 0

def handle_client(client_socket, address):
    global total_clients, total_ops, put_count, get_count, read_count, err_count
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
            
            with lock:
                total_ops += 1  # 增加操作计数
                if op == "P":
                    if key in tuple_space:
                        response = f"ERR {key} already exists"
                    else:
                        tuple_space[key] = value
                        response = f"OK ({key}, {value}) added"
                elif op == "R":
                    if key in tuple_space:
                        response = f"OK ({key}, {tuple_space[key]}) read"
                    else:
                        response = f"ERR {key} does not exist"
                elif op == "G":
                    if key in tuple_space:
                        val = tuple_space.pop(key)
                        response = f"OK ({key}, {val}) removed"
                    else:
                        response = f"ERR {key} does not exist"
                else:
                     response = "ERR unknown operation"

        # 加上响应协议格式
        full_response = f"{len(response)+4:03d} {response}"
        client_socket.send(full_response.encode())

    except Exception as e:
        print(f"[ERR] {e}")
    
    client_socket.close()

def print_stats():
    while True:
        time.sleep(10)  # 每10秒输出一次统计信息
        with lock:
            num_tuples = len(tuple_space)
            key_lengths = [len(k) for k in tuple_space.keys()]
            value_lengths = [len(v) for v in tuple_space.values()]
            avg_key = sum(key_lengths) / len(key_lengths) if key_lengths else 0
            avg_val = sum(value_lengths) / len(value_lengths) if value_lengths else 0
            avg_tuple = avg_key + avg_val

            print("\n--- Server Stats ---")
            print(f"Tuples: {num_tuples}")
            print(f"Avg key size: {avg_key:.2f}")
            print(f"Avg value size: {avg_val:.2f}")
            print(f"Avg tuple size: {avg_tuple:.2f}")
            print(f"Total clients: {total_clients}")
            print(f"Total operations: {total_ops}")
            print(f"PUT: {put_count}, GET: {get_count}, READ: {read_count}, ERR: {err_count}")
            print("---------------------\n")
            
def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", port))
    server.listen(5)
    print(f"[SERVER] Listening on port {port}...")

# 启动后台线程打印统计信息
    stats_thread = threading.Thread(target=print_stats, daemon=True)
    stats_thread.start()

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
