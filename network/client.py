import socket as soc
import os
import time
from network import tools
#import tools
from threading import Thread

FirstNumToCheck = 256
SecondNumToCheck = 256
port=2272
BUFFER=1024

def runClient(fast):
    if (fast):
        print('Quick Scan...')
        batch(tools.parseIP(tools.ourIp, 2))
        print('Done')
    print('Scanning...')
    for f in range(FirstNumToCheck):
        batch(f)
    print('Done')

def batch(f):
    threads = list()
    #print('Starting Batch ' + str(f))
    for sec in range(SecondNumToCheck):
        clientThread = Thread(target=connect, args=(f, sec,))
        threads.append(clientThread)
        clientThread.start()
    for thread in threads:
        thread.join()

def makeReceiveFolder():
    try:
        os.makedirs("Received")
    except:
        pass


def connect(first,second):
    if tools.ourIp == tools.genIp(first, second):
        #print('hello me')
        pass
    else:
        try:
            checkIp = tools.genIp(first,second)
            for file in getfiles():
                s = soc.socket()
                s.settimeout(.2) # if thread error, change this value
                s.connect((checkIp,port))
                sendFile(file,s)
                s.close()
            print('Connection to -> ' + checkIP)
        except:
            pass

def getfiles():
    files = []
    dirlist = ['ToSend']
    while len(dirlist) > 0:
        for (dirpath, dirnames, filenames) in os.walk(dirlist.pop()):
            dirlist.extend(dirnames)
            files.extend(map(lambda n: os.path.join(*n), zip([dirpath] * len(filenames), filenames)))
    return files

def sendFile(FileName,s):
    if (FileName == ''):
        return
    ourHash = tools.hash(FileName) + '0'
    s.send(b'Sending File')
    recv = s.recv(BUFFER).decode()
    if (recv != 'Receive Ready'):
        print("Receive Not Ready")
        print("Received: " + recv)
        return
    #Remove Start of file name
    FileName = FileName[FileName.find('/')+1:len(FileName)]
    FileName = FileName[FileName.find('\\')+1:len(FileName)]
    #Send and confirm File name
    s.send(FileName.encode())
    confirm = s.recv(BUFFER).decode()
    if (confirm != 'FNR'):
        print('Connected to unrecognized client, they sent:')
        print(confirm)
        return 
    #Does server have file
    s.send(b'File Status')
    serverHash = s.recv(BUFFER).decode()
    if (ourHash == serverHash):
        s.send("Match".encode())
    else:
        s.send("No Match".encode())
    #Send if file is incorrect
    if (serverHash != ourHash):
        f = open (str("ToSend/" + FileName), "rb")
        l = f.read(BUFFER)
        while (l):
            s.send(l)
            l = f.read(BUFFER)
    print(s.recv(BUFFER).decode())

if __name__ == '__main__':
    makeReceiveFolder()
    runClient(True) #fast and slow