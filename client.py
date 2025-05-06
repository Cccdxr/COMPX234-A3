import socket
import sys

def encode_request(command: str) -> str:
    # Calculate total length (after adding prefix)
    body = command.strip()
    total_len = len(body) + 4  # 3 digits for length + a space
    return f"{total_len:03d} {body}"

# Send a request to the server and receive the response
def send_request(host, port, request_line):
    # Convert operation code: PUT -> P, READ -> R, GET -> G
    parts = request_line.strip().split(" ", 1) # Split operation and key/value
    if len(parts) >= 1:
        op = parts[0].upper()
        if op == "PUT":
            request_line = "P " + parts[1] if len(parts) > 1 else "P"
        elif op == "READ":
            request_line = "R " + parts[1] if len(parts) > 1 else "R"
        elif op == "GET":
            request_line = "G " + parts[1] if len(parts) > 1 else "G"
    
    request_msg = encode_request(request_line)# Encode the request

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create TCP client socket
    client.connect((host, port)) # Connect to server
    client.send(request_msg.encode()) # Send the request message


    response = client.recv(1024).decode() # Receive server response
    print(f"Request: {request_line}")
    print(f"Response: {response}\n")

    client.close()

# Main function to parse command-line arguments and start the client
def main():
    if len(sys.argv) < 4:
        print("Usage:")
        print("  python client.py <host> <port> <request>")
        print("  python client.py <host> <port> -f <filename>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    
    if sys.argv[3] == "-f": # File mode
        if len(sys.argv) != 5:
            print("Usage: python client.py <host> <port> -f <filename>")
            sys.exit(1)
        filename = sys.argv[4]
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:  # Skip empty lines
                        send_request(host, port, line)
        except FileNotFoundError:
            print(f"File not found: {filename}")
            sys.exit(1)
    else:
        request_line = sys.argv[3] # Single request
        send_request(host, port, request_line)


if __name__ == "__main__":
    main()
