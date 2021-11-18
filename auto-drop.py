from threading import Thread
from network import server
from network import client
from network import tools

if __name__ == '__main__':
    '''
    Main auto-drop file is used to run both server and client simultaneously.
    Each is threaded separately so the user can send and receieve files at the
    same time.
    '''
    serverThread = Thread(target=server.runServer)
    clientThread = Thread(target=client.runClient,args=(True,))

    serverThread.start()
    clientThread.start()

    clientThread.join()
    serverThread.join()