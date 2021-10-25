import socket as soc
from threading import Thread

def runServer():
    host=''
    port=22722
    server_socket = soc.socket()
    server_socket.bind((host,port))
    server_socket.listen(10) # Listen to two clients
    while 1:
        #Warning, not final code in any way
        conn, addr = server_socket.accept()
        print('Connection from: ' + str(addr))
        thread = Thread(target=handleClient, args=conn)
        conn.close()

def handleClient(conn):
    while 1:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("from connected client: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())


if __name__ == '__main__':
    runServer()