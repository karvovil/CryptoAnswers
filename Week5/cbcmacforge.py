from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from Crypto.Util.strxor import strxor

zeroiv = bytes(16)

def validate(key, message):
    data = message[:-32]
    tag = message[-16:]
    iv = message[-32:-16]
    cipher = AES.new(key, AES.MODE_CBC, iv = iv)
    ct = cipher.encrypt(pad(data, AES.block_size))

    validtag = ct[-16:]
    if validtag == tag:
        print('Valid!')

def validate0(key, data, tag):
    cipher = AES.new(key, AES.MODE_CBC, iv = zeroiv)
    ct = cipher.encrypt(data)
    validtag = ct[-16:]
    if validtag == tag:
        print('Valid!')


key = get_random_bytes(16)
data = b'from=alice;to=bob=amount=40;'
iv = get_random_bytes(16)

cipher = AES.new(key, AES.MODE_CBC, iv = iv)
ct = cipher.encrypt(pad(data, AES.block_size))
tag = ct[-16:]
message = data+iv+tag   

data = message[:-32]
iv = message[-32:-16]
tag = message[-16:]#--> first block can be modified
newdata = b'wrom=alice;to=bob=amount=40;'

newivbyte = iv[0]^data[0]^newdata[0]
newiv = newivbyte.to_bytes(1, 'big') + iv[1:]
newmessage = newdata+newiv+tag

validate(key,newmessage)


#Neeeext
key = get_random_bytes(16)
a =  pad(b'this is dataaaaaaaaaaaaaaaaaaaa', 16)
b =  pad(b'There might be even more bytes here', 16)
ab = a+b

cipher = AES.new(key, AES.MODE_CBC, iv = zeroiv)
ct1 = cipher.encrypt(a)
atag = ct1[-16:]

cipher = AES.new(key, AES.MODE_CBC, iv = zeroiv)
ct2 = cipher.encrypt(b)
btag = ct2[-16:]

cipher = AES.new(key, AES.MODE_CBC, iv = zeroiv)
ct3 = cipher.encrypt(ab)
abtag = ct3[-16:]

newdata1 = a + strxor(atag,b[:16]) + b[16:]
newdata2 = ab + strxor(abtag,a[:16]) + a[16:]

validate0(key,newdata1,btag)
validate0(key,newdata2,atag)




