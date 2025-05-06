# COMPX234-A3

# COMPX234-A3: Tuple Space Client-Server System

This project implements a multithreaded client-server system using Python TCP sockets for COMPX234 Assignment 3. The client connects to a central server and performs operations on a shared key-value store (tuple space).

##  Features

- Server handles multiple client connections using threads.
- Client reads requests from a file and waits synchronously for responses.
- Tuple space supports unique keys and string values.
- Operations supported:
  - `PUT k v`: Insert a tuple
  - `READ k`: Read a tuple without removing
  - `GET k`: Read and remove a tuple
- Server prints usage statistics every 10 seconds.
- Robust error handling and protocol enforcement.

##  Files

- `server.py` — Server implementation
- `client.py` — Client implementation
- `README.md` — This file
- `client.txt`  — Request input file

##  Protocol

### Request format
- `NNN R key`
- `NNN G key`
- `NNN P key value`

Where `NNN` is the message length in 3-digit format.

### Response format
- `NNN OK (key, value) added`
- `NNN OK (key, value) read`
- `NNN OK (key, value) removed`
- `NNN ERR key already exists`
- `NNN ERR key does not exist`

##  Usage

### Start the server
```bash
python server.py <port>
# Example
python server.py 51234
```

### Start the client
```bash
python client.py <host> <port> -f <filename>
# Example
python client.py localhost 51234 -f test-workload-1/test-workload/client_1.txt  
```

The client will read each line from the request file and send it to the server.

##  Server Threads

- Server uses `threading` module to spawn a new thread for each client.
- Thread safety ensured using `threading.Lock()`.

##  Server Stats

Printed every 10 seconds:
- Number of tuples
- Average tuple/key/value size
- Total clients
- Total operations
- Counts of PUT, READ, GET, and ERR

##  Constraints

- Max key/value length: 999 characters.
- Max total message length: 999 bytes.
- Invalid lines in the request file are ignored with an error printed.

##  Example Client Output

```
Request: G silvertip
Response: 032 ERR silvertip does not exist

Request: G michel_montaigne
Response: 039 ERR michel_montaigne does not exist

Request: P hard_liquor an alcoholic beverage that is distilled rather than fermented
Response: 089 OK (hard_liquor, an alcoholic beverage that is distilled rather than fermented) added

Request: P al_aqabah Jordan's port; located in southwestern Jordan on the Gulf of Aqaba
Response: 092 OK (al_aqabah, Jordan's port; located in southwestern Jordan on the Gulf of Aqaba) added

Request: R mulberry_tree
Response: 036 ERR mulberry_tree does not exist
```

##  Requirements

- Python 3.10
- No external dependencies

## 🛠️ Development Notes

- Commit history should show incremental development.
- Built independently for academic purposes.
- Proper synchronization handles concurrency issues.

##  License

This project is developed for COMPX234 coursework and is for educational use only.
