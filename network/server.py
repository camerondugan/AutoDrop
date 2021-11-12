import socket as soc
import _thread
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
        _thread.start_new(handleAClient, (conn,))

def handleAClient(s):
    #handle client commands
    if (s.recv(BUFFER).decode() == 'Sending File'):
        s.send(b'Recieve Ready')
        FileName = s.recv(BUFFER).decode()
        FileName = 'Recieved/' + FileName
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
            if(hashMatches == 'NoMatch'):
                if not f:
                    f = open(FileName,'wb')
                #Write File
                l = s.recv(BUFFER)
                while (l):
                    f.write(l)    
                    l = s.recv(BUFFER)
        else:
            s.close()
    else:
        conn.close()


if __name__ == '__main__':
    runServer()