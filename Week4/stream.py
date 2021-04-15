from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import binascii
from Crypto.Cipher import Salsa20
import time

secret = b'*Thirty-two byte (256 bits) key*'
ntwice = b'12345678'
cipher1 = Salsa20.new(key=secret,nonce=ntwice)
cipher2 = Salsa20.new(key=secret,nonce=ntwice)
msg = cipher1.encrypt(b'Move the tables to the patio as soon as possible!')
msg2 = cipher2.encrypt(b'Move the chairs to the house as soon as possible!')
print(msg.hex())
print(msg2.hex())

secret1 = b'123456789x123456789y123456789z11'
secret2 = b'asdfghjkl1asdfghjkl2asdfghjklz12'
ntwice = b'12345678'
cipher1 = Salsa20.new(key=secret1,nonce=ntwice)
cipher2 = Salsa20.new(key=secret2,nonce=ntwice)
msg =  cipher1.encrypt(b'Alabamamamabamaalaa')
msg2 = cipher2.encrypt(b'Alabamamamabamaalab')
print(msg.hex())
print(msg2.hex())

data = get_random_bytes(2**27)
secret = b'*Thirty-two byte (256 bits) key*'

aescbc = AES.new(secret, AES.MODE_CBC)
aesctr = AES.new(secret, AES.MODE_CTR)
salsa = Salsa20.new(key=secret1)


start = time.time()
cbcText = aescbc.encrypt(data)
end = time.time()
print(1000*(end-start))

start = time.time()
ctrText = aesctr.encrypt(data)
end = time.time()
print(1000*(end-start))

start = time.time()
salsaText = salsa.encrypt(data)
end = time.time()
print(1000*(end-start))


