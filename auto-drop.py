from threading import Thread
from network import server
from network import client
from network import tools

if __name__ == '__main__':
    serverThread = Thread(target=server.runServer)
    clientThread = Thread(target=client.runClient,args=(True,))

    serverThread.start()
    clientThread.start()

    clientThread.join()
    serverThread.join()