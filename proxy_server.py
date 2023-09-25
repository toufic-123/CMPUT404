''' 
a proxy is a middle man. instead of client connecting directly to the server - they connect to the 
proxy which connects to the client. the proxy takes a resquest from the user and sends that to the server
and then send the response back to the user. 
benefit:
 - is that ip and port is hidden
 - security can all be handled on the proxy instead of on the main server

 
e.g.
user -> proxy
proxy -> google
proxy <- google
user <- proxy
'''
import socket
from threading import Thread

PROXY_SERVER_HOST = "localhost"
PROXY_SERVER_PORT = 8080

BYTES_TO_READ = 4096

def send_request(host, port, request):


    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as client_socket:

        client_socket.connect((host,port))
        client_socket.send(request)
        print("sent")
        client_socket.shutdown(socket.SHUT_WR)

        data = client_socket.recv(BYTES_TO_READ)
        result = b'' + data
        while(len(data) > 0):
            data = client_socket.recv(BYTES_TO_READ)
            result += data
        
        return result

def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")

        request = b''
        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            print(data)
            request += data
        response = send_request("www.google.com", 80, request)
        conn.sendall(response)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST,PROXY_SERVER_PORT))


        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2)

        conn, addr = server_socket.accept()

        handle_connection(conn,addr)




def start_threaded_sever():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(PROXY_SERVER_HOST,PROXY_SERVER_PORT)
        server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        server_socket.listen(2) # only allow 2 at a time

        while True:
            conn, addr = server_socket.accept()
            thread = Thread(target=handle_connection,args=(conn,addr))
            thread.run()


start_threaded_sever()