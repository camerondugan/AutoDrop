#Things like network scanning and misc. methods
import socket as soc

ourPort = 0000
#Change below
FirstNumToCheck = 255
SecondNumToCheck = 255
ourIp='127.0.0.1'
try:
    s = soc.socket(soc.AF_INET, soc.SOCK_DGRAM)
    s.connect(('192.0.0.1',1))
    ourIp=s.getsockname()[0]
except:
    print("failed to get ip")
    pass

#ourIp = soc.gethostbyname(soc.gethostname())

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

#Returns an int subSection from the ip
def parseIP(ip,section):
    #Bug, doesn't work for 0th index
    start = 0
    end = 0
    i = 0
    periods = 0
    for c in ip:
        if c == '.':
            periods += 1
            if (periods == section):
                start = i+1
            elif (periods == section+1):
                end = i
        i += 1
    if end == 0:
        end == i
    return int(ip[start:end])

#Currently just prints all the ports we want to check
def scan():
    for f in range(FirstNumToCheck):
        for s in range(SecondNumToCheck):
            print(genIp(f,s))


if __name__ == '__main__':
    print(ourIp)
    scan()