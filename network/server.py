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
    FileName = conn.recv(1024).decode()
    print(FileName)

    f = open("Recieved/"+FileName,'wb') # Open in binary
    while (True):
        # We receive and write to the file.
        l = sc.recv(1024)
        while (l):
            f.write(l)    
    conn.close()


if __name__ == '__main__':
    runServer()