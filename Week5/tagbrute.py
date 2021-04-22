from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import time

key = get_random_bytes(16)
data1 = get_random_bytes(4)
cipher1 = AES.new(key, AES.MODE_CCM, mac_len = 4)

nonce = cipher1.nonce
ciphertext1, tag1 = cipher1.encrypt_and_digest(data1)
print('data1: ' + data1.hex())
print('tag1: ' + tag1.hex())

start = time.time()
for d in range(2**32):
    data2 = d.to_bytes(4, byteorder='big')
    cipher2 = AES.new(key, AES.MODE_CCM, mac_len = 4, nonce=nonce)
    ciphertext2, tag2 = cipher2.encrypt_and_digest(data2)
    if tag2[:3] == tag1[:3]:
        end = time.time()
        break

print('data2: ' + data2.hex())
print('tag2: ' + tag2.hex())
print('time: ',end-start)

