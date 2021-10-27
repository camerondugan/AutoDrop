import socket as soc

def runClient():
    host='127.0.0.1'
    port=2272

    while True:
        try:
            s = soc.socket()
            s.connect((host,port))
            s.send(b'Hello')
            sleep(2)
            s.close()
        except:
            pass


if __name__ == '__main__':
    runClient()