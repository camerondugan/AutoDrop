#Things like network scanning and misc. methods
import socket as soc
import hashlib

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

#tests gen ip (doesn't actually scan)
def scan():
    for f in range(FirstNumToCheck):
        for s in range(SecondNumToCheck):
            print(genIp(f,s))

'''
sha256 file hash generator adapted from 
https://www.quickprogrammingtips.com/python/how-to-calculate-sha256-hash-of-a-file-in-python.html
'''
def hash(filename):
    ans = ""
    sha256_hash = hashlib.sha256()
    with open(filename,"rb") as f:
        for block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(block)
            ans += sha256_hash.hexdigest()
    return ans

if __name__ == '__main__':
    print(ourIp)
    print(hash('./network/client.py'))
    #scan()