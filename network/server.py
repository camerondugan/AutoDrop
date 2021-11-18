import socket as soc
import _thread
import os
from network import tools
#import tools

BUFFER=1024

def runServer():
    host=''
    port=2272
    server_socket = soc.socket()
    server_socket.bind((host,port))
    server_socket.listen(10) # Listen to two clients
    while 1:
        conn, addr = server_socket.accept()
        print('Connection from: ' + str(addr))
        _thread.start_new(handleAClient, (conn,addr,))

def makeUserFolder(ip):
    try:
        os.makedirs(os.path.join("Received" ,ip))
    except:
        pass

def handleAClient(s,addr):
    if (addr[0] == tools.ourIp):
        return
    #handle client commands
    if (s.recv(BUFFER).decode() == 'Sending File'):
        s.send(b'Receive Ready')
        FileName = s.recv(BUFFER).decode()
        makeUserFolder(addr[0])
        FileName = 'Received/' + addr[0] + '/' + FileName
        s.send(b'FNR')
        fileHash = 'NoFile'
        try:
            fileHash = tools.hash(FileName) + '0'
        except:
            pass
        f = None
        try: #no file
            f = open(FileName,'xb') # Open as binary
        except: #file exists
            pass
        request = s.recv(BUFFER).decode()
        if (request == 'File Status'):
            s.send(fileHash.encode())
            hashMatches = s.recv(BUFFER).decode()
            if(hashMatches == 'No Match'):
                if not f:
                    f = open(FileName,'wb')
                #Write File
                l = s.recv(BUFFER)
                while (l):
                    f.write(l)    
                    l = s.recv(BUFFER)
            s.send(b'File Received')
        else:
            print("bad connection or client")
    s.close()


if __name__ == '__main__':
    runServer()