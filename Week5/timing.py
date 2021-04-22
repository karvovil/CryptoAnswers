import subprocess
import json 
from base64 import b64decode, b64encode
from time import time

with open("ciphertext", "rb") as file:
    cipherbinary = file.read()
file.close() 
ciphertext = b64encode(cipherbinary).decode()

def mactime(mac):
    data = {
    "sender": "Bob",
    "receiver": "Alice",
    "data": ciphertext,
    "tag": mac 
    }
    with open("data.json", "w") as f:
        json.dump(data, f)
    f.close()

    start = time()
    for _ in range(20):
        result = subprocess.run(["./authenticator" ,"-f", "data.json"], capture_output=True)
        if(result.returncode == 0):
            print(result)
            quit()
    end = time()

    return(end-start)

def findslowest(verifiedBytes):
    slowestTime = 0
    slowestByte = ''
    for n in range(256):
        testByte = n.to_bytes(1, byteorder='big').hex()
        testTime = mactime( verifiedBytes + testByte )
        if testTime > slowestTime:
            slowestByte = testByte
            slowestTime = testTime 
    findslowest(verifiedBytes + slowestByte)
        
findslowest('')


#0d8476f2314e
