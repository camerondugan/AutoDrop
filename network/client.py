import socket as soc
import os
from network import tools
#import tools
from threading import Thread


FirstNumToCheck = 256
SecondNumToCheck = 256
port=2272

def runClient(fast):
    if (fast):
        batch(tools.parseIP(tools.ourIp, 2))
    for f in range(FirstNumToCheck):
        batch(f)

def batch(f):
    threads = list()
    print("Starting Batch " + str(f))
    for sec in range(SecondNumToCheck):
        clientThread = Thread(target=connect, args=(f, sec,))
        threads.append(clientThread)
        clientThread.start()
    for thread in threads:
        thread.join()

def connect(first,second):
    #if tools.ourIp == tools.genIp(first, second):
        #print("hello me")
        #return
    try:
        print('checking connection on ' + tools.genIp(first, second))
        s = soc.socket()
        s.settimeout(.2) # if thread error, change this value
        s.connect((tools.genIp(first,second),port))
        for file in getfiles():
            sendFile(file,s)
        s.close()
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
    FileName = FileName[FileName.find('/')+1:len(FileName)]
    print(FileName)
    s.send(FileName.encode())
    confirm = s.recv(1024).decode()
    if (confirm != 'FNR'):
        print("Not our software!")
        print(confirm)
        return 
    f = open (str("ToSend/" + FileName), "rb")
    l = f.read(1024)
    while (l):
        s.send(l)
        l = f.read(1024)
    print("success")


if __name__ == '__main__':
    print(getfiles())
    connect(60, 155)
    #runClient(True)
    #runClient(False)