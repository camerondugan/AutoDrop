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
    if (FileName):
        FileName = "Recieved/" + FileName
        conn.send(b'FNR')
    f = open(FileName,'xb') # Open in binary
    # We receive and write to the file.
    l = conn.recv(1024)
    while (l):
        f.write(l)    
        l = conn.recv(1024)
    conn.close()


if __name__ == '__main__':
    runServer()