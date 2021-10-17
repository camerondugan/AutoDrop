from threading import Thread

def runServer():
    while True:
        print('running server')

def runClient():
    while True:
        print('running client')

if __name__ == '__main__':
    #Multithreading basics
    serverThread = Thread(target=runServer)
    serverThread.start()
    clientThread = Thread(target=runClient)
    clientThread.start()

    #Eventually...
    # serverThread.join()
    # clientThread.join()