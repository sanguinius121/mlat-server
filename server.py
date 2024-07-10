import socket
import threading
import pickle


HEADER = 64
PORT = 5050
IP_TAILSCALE = '100.104.228.105'
SERVER = socket.gethostbyname(IP_TAILSCALE)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

#creat a socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

file_lock = threading.Lock()


def handle_client(conn, addr):
    print(f"[NEW CONNECTION: ] {addr} connected.")
    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                print(msg_length)
                msg_length = int(msg_length)
                msg = conn.recv(msg_length)
                if len(msg) == msg_length:
                    try:
                        msg_decode = pickle.loads(msg)
                        print(msg_decode)
                        with file_lock:
                            with open('server_data_3.txt', 'a') as file:
                                file.write(str(msg_decode) + '\n')
                    except (pickle.UnpicklingError, EOFError, AttributeError, ImportError, IndexError) as e:
                        print(f"Error unpickling message: {e}")
                        continue  # Skip this message and continue with the next
                else:
                    continue
                if msg_decode == DISCONNECT_MESSAGE:
                    connected = False
        except Exception as e:
            print(f"Error of decoding length: {e}")
            continue #skipping the header and continue
    conn.close()


def start():
    server.listen()
    print('Server is running on : ' + str(SERVER))
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

start()
