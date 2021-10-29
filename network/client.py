import socket as soc
import tools
from threading import Thread

FirstNumToCheck = 256
SecondNumToCheck = 256
port=2272

def runClient(fast):
    if (fast):
        batch(tools.parseIP(tools.ourIp, 2))
        return
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
    try:
        print('checking connection on ' + tools.genIp(first, second))
        s = soc.socket()
        s.settimeout(.2) # if thread error, change this value
        s.connect((tools.genIp(first,second),port))
        s.send(b'test.txt')
        confirm = s.recv(1024).decode()
        print(confirm)
        f = open ("ToSend/test.txt", "rb")
        l = f.read(1024)
        while (l):
            s.send(l)
            l = f.read(1024)
        print("success")
        s.close()
    except:
        pass

if __name__ == '__main__':
    #connect(58, 145)
    runClient(True)
    #runClient(False)