import socket as soc
import os
import time
from network import tools
from threading import Thread

maxThird = 256
maxFourth = 256
port=2272
BUFFER=1024
knownHosts = []

'''
runClient is a quicker scan which checks IPs in your immediate sub-network before
parsing through all systems on the network for connections
'''
def runClient(fast):
    if (fast):
        print('Quick Scan...')
        batch(tools.parseIP(tools.ourIp, 2))
        print('Done')
    print('Scanning...')
    for f in range(maxThird):
        batch(f)
    print('Done')

'''
batch divides up all the IPs the client needs to surf through into separate threads
so the process doesn't take as long
'''
def batch(f):
    threads = list()
    #print('Starting Batch ' + str(f))
    for sec in range(maxFourth):
        reconnect()
        '''
        also reconnects to previously connected clients from earlier
        in the session to ensure everything is up to date
        '''
        clientThread = Thread(target=connect, args=(tools.genIp(f, sec),))
        threads.append(clientThread)
        clientThread.start()
    for thread in threads:
        thread.join()


'''
creates the directory to receive files if not already existant
'''
def makeReceiveFolder():
    try:
        os.makedirs("Received")
    except:
        pass

'''
attempts to connect to the given IP address, if the IP is the same as the clients,
the connection is aborted
'''
def connect(checkIp):
    if tools.ourIp == checkIp:
        #This is our ip, don't try to connect
        pass
    else:
        try:
            for file in getfiles():
                time.sleep(5)
                s = soc.socket()
                s.settimeout(.2) # if thread error, change this value
                s.connect((checkIp,port))
                sendFile(file,s)
                s.close()
            print('Connection to -> ' + checkIp)
            if not knownHosts.__contains__(checkIp):
                knownHosts.append(checkIp)
        except:
            pass

'''
reconnect attempts to establish connections with known hosts
'''
def reconnect():
    for serverIp in knownHosts:
        clientThread = Thread(target=connect, args=(serverIp,))
        threads.append(clientThread)
        clientThread.start()

'''
retrieves the files that need to be sent to the other user from the ToSend directory
'''
def getfiles():
    files = []
    dirlist = ['ToSend']
    while len(dirlist) > 0:
        #iterates through the directory and obtains all file names
        for (dirpath, dirnames, filenames) in os.walk(dirlist.pop()):
            dirlist.extend(dirnames)
            files.extend(map(lambda n: os.path.join(*n), zip([dirpath] * len(filenames), filenames)))
    return files

'''
encodes and sends the file passed in to the other user's server
'''
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
        sendBits(FileName,s)
    print(s.recv(BUFFER).decode())

def sendBits(FileName, s):
    f = open (str("ToSend/" + FileName), "rb")
    l = f.read(BUFFER)
    while (l):
        s.send(l)
        l = f.read(BUFFER)

if __name__ == '__main__':
    makeReceiveFolder()
    runClient(True) #fast and slow