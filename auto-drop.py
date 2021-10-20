from threading import Thread
from network import server
from network import client
from network import tools

if __name__ == '__main__':
    serverThread = Thread(target=server.runServer)
    clientThread = Thread(target=client.runClient)

    serverThread.start()
    clientThread.start()

    serverThread.join()
    clientThread.join()