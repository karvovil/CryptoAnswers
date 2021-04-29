import subprocess
from Crypto.PublicKey import RSA
import json

file = open('files/alice.pub', 'r')
pubkey = RSA.import_key( file.read() ) 

evilmessage = int.from_bytes(b'_p', "big")  

for r in range(99999999999):
    newint = pow(r, pubkey.e, pubkey.n)*evilmessage % pubkey.n
    newbytes = newint.to_bytes((newint.bit_length() + 7) // 8,'big')
    if newbytes[:2] == b'_n' :
        break

with open("files/file1", "wb") as file:
    file.write(newbytes)
    file.close()
    
result = subprocess.run(["files/./alice" ,'-j',"-f", 'files/file1'], capture_output=True) 
dick = json.loads(result.stdout.decode('ascii'))
sig = int(dick['signature'], 16)

evilsig = sig * pow(r,-1,pubkey.n)

print(hex(newint))
print(hex(sig))

print(pow(evilsig,pubkey.e,pubkey.n))
print(evilmessage)