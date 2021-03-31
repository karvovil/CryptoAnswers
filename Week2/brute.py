from Crypto.Cipher import Blowfish
from struct import pack
from Crypto.Random import get_random_bytes

key = b'00' + get_random_bytes(2)
cipher = Blowfish.new(key, Blowfish.MODE_EAX)
plaintext = b'Takes about 20 seconds to brute force this open'


bs = Blowfish.block_size
plen = bs - len(plaintext) % bs
padding = [plen]*plen
padding = pack('b'*plen, *padding)

nonce = cipher.nonce
ciphertext, tag = cipher.encrypt_and_digest(plaintext + padding)
del key, plaintext, cipher

for n in range(2**16):
    key = b'00' + n.to_bytes(2, 'little')
    cipher2 = Blowfish.new(key, Blowfish.MODE_EAX, nonce = nonce)
    try:
        plaintext = cipher2.decrypt_and_verify(ciphertext, tag)
        print("Authentic message:", plaintext)
        break
    except ValueError:
            pass
               