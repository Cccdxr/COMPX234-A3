import socket
import sys

def main():
    if len(sys.argv) != 4:
        print("Usage: python client.py <host> <port> <request>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    request = sys.argv[3]

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.send(request.encode())
    client.close()

if __name__ == "__main__":
    main()
