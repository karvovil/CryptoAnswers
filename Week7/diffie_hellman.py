from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import getPrime, getStrongPrime, isPrime
from Crypto.Random import get_random_bytes
from typing import Union
from hashlib import sha256
import random
# Methods for handling encryption and decryption of data, no need to edit


def secret_into_aes_key(secret: int) -> bytes:
    """Convert arbitrary integer for suitable key for AES-CBC by using SHA256 digest"""
    m = sha256()
    m.update(secret.to_bytes((secret.bit_length() + 7) // 8, byteorder="big"))
    return m.digest()


def encrypt_aes(data: Union[bytes, str], key: bytes) -> bytes:
    """Encrypt data after padding, by key, set IV as prefix"""
    if isinstance(data, str):
        data = data.encode("ASCII")
    elif not isinstance(data, bytes):
        raise ValueError("Encryptable data must be in 'bytes' or 'string' format.")
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    return cipher.iv + ciphertext


def decrypt_aes(data: bytes, key: bytes) -> bytes:
    """Extract IV, decrypt data by key and unpad"""
    if not isinstance(data, bytes):
        raise ValueError("Decryptable data must be in 'bytes' format.")
    IV = data[: AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv=IV)
    plaintext = unpad(cipher.decrypt(data[AES.block_size :]), AES.block_size)
    return plaintext

def getSafePrime(length):

    p = getPrime(length)
    
    while not isPrime((p-1)//2):
        p = getPrime(length)
    return p

class SingleParty:
    """Abstract class for common attributes for each party, e.g. Alice, Bob and Eve. Add public values here"""

    # TODO Choose public values, however it might be that some values are better than others

    g: int = 2

    p_modulus: int = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF  # prime, usually 2048 bits to provide enough security 

    _G: int = None  # Shared secret, calculated later

    def encrypt(self, data: bytes, G: int = None) -> bytes:
        """Encrypt data, use established shared secret as key by default if no G parameter provided"""
        return encrypt_aes(data, secret_into_aes_key(G if G else self._G))

    def decrypt(self, data: bytes, G: int = None) -> bytes:
        """Decrypt data, use established shared secret as key by default if no G parameter provided"""
        return decrypt_aes(data, secret_into_aes_key(G if G else self._G))


# Define private exponents for Bob, Alice and Eve
# Check how to get primes https://pycryptodome.readthedocs.io/en/latest/src/util/util.html#module-Crypto.Util.number

# Select a prime p where (p – 1) / 2 is also prime and that p is large enough


class Alice(SingleParty):

    _P: int = getSafePrime(256)  # Private exponent
    A: int = 0

    def __init__(self):
        super(SingleParty).__init__()  

    def set_A(self):
        Alice.A = pow(Alice.g, Alice._P, Alice.p_modulus)
        pass

    def set_G(self, B: int):
        Alice._G = pow(B,Alice._P,Alice.p_modulus)   
        pass


class Bob(SingleParty):

    _P: int = getSafePrime(256)  # Private exponent
    B: int = 0

    def __init__(self):
        super(SingleParty).__init__()

    def set_B(self):
        """TODO Implement calculation of B"""
        Bob.B = pow(Bob.g, Bob._P, Bob.p_modulus)
        pass

    def set_G(self, A: int):
        """TODO Derive G from A (G is shared secret)"""
        Bob._G = pow(A,Bob._P,Bob.p_modulus)
        pass


class Eve(SingleParty):
    """
    TODO
    Eve needs methods and values for both Alice and Bob:
    - two private exponents
    - two shared keys
    - methods for implementing the key exchange and storing A, B, C and D (Check course book from the page 210)
    Note that Eve must change parameters when decrypting/encrypting data
    """

    A: int = 0  # A from Alice
    C: int = 0  # C for Bob
    B: int = 0  # B from Bob
    D: int = 0  # D for Alice
    _P1: int = getSafePrime(256)  # Private exponent for Alice
    _P2: int = getSafePrime(256)  # Private exponent for Bob
    _G1: int = 0  # Shared key with Alice
    _G2: int = 0  # Shared key with Bob

    def __init__(self):
        super(SingleParty).__init__()
        Eve.C = pow(Eve.g, Eve._P2, Eve.p_modulus)
        Eve.D = pow(Eve.g, Eve._P1, Eve.p_modulus)
    
    def set_G1(self, A: int):
        Eve._G1 = pow(A,Eve._P1,Eve.p_modulus)
        pass

    def set_G2(self, B: int):
        Eve._G2 = pow(B,Eve._P2,Eve.p_modulus)
        pass

    def set_G(self, party):
        if party == "Alice":
            Eve._G = Eve._G1
        if party == "Bob":
            Eve._G = Eve._G2
        pass

    # TODO add rest of the methods


# TODO you should demonstrate man-in-the-middle attack by just calling classes and their methods in correct order,
# after fullfilling the implementation(s) and adding suitable values.

# After successfull key exchange, you can finally select some data which is encrypted by Alice,
#  then decrypted by Eve, re-encrypted by Eve to pass data for Bob who finally decrypts the data

# Example use of one of the classes *without* key exchange, by just setting shared key value
#al = Alice()
#al._G = 123456
#ciphertext = al.encrypt("Hello, world!")
#print(al.decrypt(ciphertext))


al = Alice() #Alice wakes up and her private exponent is defined
al.set_A() #Alice's public value is calculated

ev = Eve() #Eve's private exponents and public values are initialized at this point
ev.set_G1(Alice.A) # Secret with Alice is calculated

bo = Bob() #Bob wakes up and his private exponent is defined
bo.set_B() #Bob's public value is calculated

bo.set_G(Eve.C) # Eve gives her public value to Bob and Bob calculates the secret 
ev.set_G2(Bob.B) # Secret with Bob is calculated

al.set_G(Eve.D) # Eve gives her public value to Alice and Alice calculates the secret


cipherA = al.encrypt("Hello") # Alice encrypts a message

ev.set_G("Alice") # G is set to the secret established with Alice
plain = ev.decrypt(cipherA) # Eve decrypts with the common secret with Alice 
print(plain)
ev.set_G("Bob") # Eve switches to Bob-mode
cipherB = ev.encrypt(plain) # Eve encrypts with the Bob-secret 

plain = bo.decrypt(cipherB) # Bob decrypts
print(plain)


