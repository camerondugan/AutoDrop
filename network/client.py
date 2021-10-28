import socket as soc
import tools
from threading import Thread

FirstNumToCheck = 256
SecondNumToCheck = 256
port=2272

def runClient():
    for f in range(FirstNumToCheck):
        threads = list()
        print("Starting Batch " + str(f))
        for sec in range(SecondNumToCheck):
            clientThread = Thread(target=connect, args=(f, sec,))
            threads.append(clientThread)
            clientThread.start()
        for thread in threads:
            thread.join()
    
    #blockSize = 300
    #while len(tQueue) > 0:
        #running = list()
        #for i in range(blockSize):
            #thread = tQueue.pop()
            #if thread:
                #running.append(thread)
                #thread.start()
        #for t in running:
            #t.join()

def connect(first,second):
    try:
    #print('checking connection on ' + tools.genIp(first, second))
        s = soc.socket()
        s.settimeout(.1)
        s.connect((tools.genIp(first,second),port))
        s.send(b'test.txt')
        f = open ("test.txt", "rb")
        l = f.read(1024)
        while (l):
            s.send(l)
            l = f.read(1024)
        print("success")
        s.close()
    except:
        pass

if __name__ == '__main__':
    #checkConnection(58, 145)
    runClient()