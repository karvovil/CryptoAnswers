import hashlib
import time
from Crypto.Random import get_random_bytes

h = get_random_bytes(5)
nexth = hashlib.md5(h).digest()

start = time.time()

while nexth[:3] != b'\x00\x00\x00':
    h = nexth
    nexth = hashlib.md5(h).digest()

end = time.time()
print(end-start)
print(h.hex() +'\n')

h = get_random_bytes(5)
nexth = hashlib.sha1(h).digest()
start = time.time()
while nexth[:3] != b'\x00\x00\x00':
    h = nexth
    nexth = hashlib.sha1(h).digest()
end = time.time()
print(end-start)
print(h.hex() +'\n')

h = get_random_bytes(5)
nexth = hashlib.sha256(h).digest()
start = time.time()
while nexth[:3] != b'\x00\x00\x00':
    h = nexth
    nexth = hashlib.sha256(h).digest()
end = time.time()
print(end-start)
print(h.hex())