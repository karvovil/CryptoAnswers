from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import binascii

data = b'12345678901234561234567890123456' 
key = get_random_bytes(16)
#key = b'1234567890123456'

aesecb = AES.new(key, AES.MODE_ECB) 
aescbc = AES.new(key, AES.MODE_CBC)
aesctr = AES.new(key, AES.MODE_CTR)

ecbText = aesecb.encrypt(data)
cbcText = aescbc.encrypt(data)
ctrText = aesctr.encrypt(data)

#aescipher2 = AES.new(key, AES.MODE_CFB, aescipher.iv)
#plaindata = aescipher2.decrypt(ciphertext)

print(binascii.hexlify(ecbText) )
print(binascii.hexlify(cbcText) )
print(binascii.hexlify(ctrText) )
print(binascii.hexlify(key) )

data = b'12345678901234561234567890123456jee'
ctrText = aesctr.encrypt(data)
print(binascii.hexlify(ctrText) )