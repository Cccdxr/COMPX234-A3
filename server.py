import socket
import threading
import time  

tuple_space = {}  # Shared tuple space
lock = threading.Lock()  # Used for thread synchronization

# Global variables for statistics
total_clients = 0
total_ops = 0
put_count = 0
get_count = 0
read_count = 0
err_count = 0

# Function to handle client requests
def handle_client(client_socket, address):
    global total_clients, total_ops, put_count, get_count, read_count, err_count
    print(f"[+] Connected with {address}")
    
    with lock:
        total_clients += 1  # Increment total client count for each connection
    try:
        data = client_socket.recv(1024).decode() # Receive client request
        if not data:
            return

        print(f"[REQ] {data.strip()}")

        # Parse protocol content
        size_str = data[:3] # Extract message length
        message = data[4:] # Extract message body
        parts = message.strip().split(" ", 2) # Extract operation, key, and value

        if len(parts) < 2:
            response = "ERR invalid message format" # Invalid format
        else:
            op, key = parts[0], parts[1]
            value = parts[2] if len(parts) == 3 else ""
            
            with lock:
                total_ops += 1  # Increment total operation count
                if op == "P":
                    if key in tuple_space:
                        response = f"ERR {key} already exists"
                        err_count += 1
                    else:
                        tuple_space[key] = value
                        response = f"OK ({key}, {value}) added"
                        put_count += 1
                        print(f"[DEBUG] Current tuple space: {tuple_space}")
                        print(f"[DEBUG] PUT count: {put_count}, GET count: {get_count}, READ count: {read_count}")
                elif op == "R":
                    read_count += 1  # Count READ regardless of key existence
                    if key in tuple_space:
                        response = f"OK ({key}, {tuple_space[key]}) read"
                        read_count += 1
                    else:
                        response = f"ERR {key} does not exist"
                        err_count += 1
                elif op == "G":
                    get_count += 1  # Count GET regardless of key existence
                    if key in tuple_space:
                        val = tuple_space.pop(key)
                        response = f"OK ({key}, {val}) removed"
                        get_count += 1
                        print(f"[DEBUG] Current tuple space after G: {tuple_space}")
                    else:
                        response = f"ERR {key} does not exist"
                        err_count += 1
                else:
                     response = "ERR unknown operation"
                     err_count += 1

        full_response = f"{len(response)+4:03d} {response}"  # Format the response
        client_socket.send(full_response.encode())

    except Exception as e:
        print(f"[ERR] {e}")
    
    client_socket.close()

# Thread function to print statistics
def print_stats():
    while True:
        print("Printing stats...")  # Debug output to confirm function call
        time.sleep(10)  # Output stats every 10 seconds
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

# Start the server and accept client connections            
def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", port))
    server.listen(5)
    print(f"[SERVER] Listening on port {port}...")

# Start background thread to print stats
    stats_thread = threading.Thread(target=print_stats, daemon=True)
    stats_thread.start()
    print("Started stats thread")  # Debug output

    while True:
        client_socket, address = server.accept() # Accept client connection
        print(f"New connection from {address}")  # Print client connection info
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_server(port)
