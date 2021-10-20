#Things like network scanning and misc. methods
import socket as soc

ourPort = 0000
#Change below
FirstNumToCheck = 10
SecondNumToCheck = 10000
ourIp = soc.gethostbyname(soc.gethostname())

def genIp(first,second):
    ip = ""
    numPeriods = 0
    for c in ourIp:
        if c == '.':
            numPeriods += 1
        if (numPeriods==2):
            break
        ip+=c
    return ip+'.'+str(first)+'.'+str(second)

#Currently just prints all the ports we want to check
def scan():
    for f in range(FirstNumToCheck):
        for s in range(SecondNumToCheck):
            print(genIp(f,s))


if __name__ == '__main__':
    scan()