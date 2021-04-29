from Crypto.Hash import SHA1
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
import os


hashes = []
f = open('files/messages.txt')
messagelines = f.read().splitlines()
for message in messagelines:
    hashes.append(SHA1.new(message.encode())) 

keys = []
keyfiles = os.listdir('files/public_keys/')
for file in keyfiles:
   file = open(os.path.join('files/public_keys/'+ file), 'r')
   keys.append( RSA.import_key( file.read() ) )


sigs = []
sigfiles = os.listdir('files/signatures/')
for file in sigfiles:
   file = open(os.path.join('files/signatures/'+ file), 'rb')
   sigs.append(file.read())


for h in range(20):
    for k in range(5):
        for s in range(20):
            try:
                pkcs1_15.new(keys[k]).verify(hashes[h], sigs[s])
                print(h+1, ' '+ keyfiles[k] +'  '+ sigfiles[s])
            except (ValueError):
                pass
