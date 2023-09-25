import socket
from threading import Thread

HOST = "127.0.0.1" # 127.0.0.1 localhost
PORT = 8080
BYTES_TO_READ = 4096

def handle_connection(conn,addr):
    with conn:
        print(f"connected by {addr}")
        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            print(data)
            conn.sendall(data)

# start single threaded echo server
def start_server():
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT))
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.listen()
        conn,addr = s.accept()
        handle_connection(conn,addr)

    # conn = socket at the client side (needs an instance of the client socket)
    # addr is the ip and port of the client (ip, port)
    # if we recv something then print it
    # when there is nothing left sendall data
    # echo server just sends back whatever it recieves

def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT))
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.listen(2)
        while True:
            conn, addr = s.accept()
            thread = Thread(target=handle_connection,args=(conn,addr))
            thread.run()

print("starting server...")
start_threaded_server()