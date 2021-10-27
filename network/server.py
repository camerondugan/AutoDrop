import socket as soc
import _thread

def runServer():
    host=''
    port=2272
    server_socket = soc.socket()
    server_socket.bind((host,port))
    server_socket.listen(10) # Listen to two clients
    while 1:
        conn, addr = server_socket.accept()
        print('Connection from: ' + str(addr))
        _thread.start_new(handleAClient, (conn,))

def handleAClient(conn):
    data = conn.recv(1024).decode()
    print("from connected client: " + str(data))
    conn.close()


if __name__ == '__main__':
    runServer()