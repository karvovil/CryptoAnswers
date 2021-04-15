import hashlib
from Crypto.Random import get_random_bytes
import time

key1 = b'\x00\x00\x00\x00\x00'
h1 = hashlib.md5(key1).digest()
key2 = get_random_bytes(5)
h2 = hashlib.md5(key2).digest()

start = time.time()

while h1[:3] != h2[:3]:
    key2 = get_random_bytes(5)
    h2 = hashlib.md5(key2).digest()

end = time.time()
print(end-start)
print(key1.hex() +'\n'+ key2.hex() +'\n')


key1 = b'\x00\x00\x00\x00\x00'
h1 = hashlib.sha1(key1).digest()
key2 = get_random_bytes(5)
h2 = hashlib.sha1(key2).digest()

start = time.time()
while h1[:3] != h2[:3]:
    key2 = get_random_bytes(5)
    h2 = hashlib.sha1(key2).digest()
end = time.time()

print(end-start)
print(key1.hex() +'\n'+ key2.hex() +'\n')


key1 = b'\x00\x00\x00\x00\x00'
h1 = hashlib.sha256(key1).digest()
key2 = get_random_bytes(5)
h2 = hashlib.sha256(key2).digest()

start = time.time()
while h1[:3] != h2[:3]:
    key2 = get_random_bytes(5)
    h2 = hashlib.sha256(key2).digest()
end = time.time()

print(end-start)
print(key1.hex() +'\n'+ key2.hex() )
