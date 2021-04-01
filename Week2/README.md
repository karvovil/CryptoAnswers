# Answer template for Crypto course, week 2
## Task 1

### Task 1.1
Private keys are generated:
```console
time openssl genpkey -out rsa1.key -algorithm RSA -pkeyopt rsa_keygen_bits:2048 
time openssl genpkey -out rsa2.key -algorithm RSA -pkeyopt rsa_keygen_bits:8192

time openssl genpkey -out esdc1.key -algorithm EC  -pkeyopt ec_paramgen_curve:P-256 
time openssl genpkey -out esdc2.key -algorithm EC  -pkeyopt ec_paramgen_curve:P-384 

time openssl genrsa -out oldkey1.pem 2048
time openssl genrsa -out oldkey2.pem 4096

time openssl dsaparam -noout -out dsa1.pem -genkey 1024
time openssl dsaparam -noout -out dsa2.pem -genkey 4096
```
Correspondning times:
```terminal
user	0m0.298s
user	0m8.026s

user	0m0.004s
user	0m0.005s

user	0m0.115s
user	0m0.558s

user	0m0.042s
user	0m2.271s
```
Public key generation:
```terminal
openssl pkey -in rsa1.key -pubout -out rsa1-public.key
openssl pkey -in rsa2.key -pubout -out rsa2-public.key

openssl pkey -in esdc1.key -pubout -out esdc1-public.key
openssl pkey -in esdc2.key -pubout -out esdc2-public.key

openssl pkey -in oldkey1.pem -pubout -out oldkey1-public.pem
openssl pkey -in oldkey2.pem -pubout -out oldkey2-public.pem

openssl pkey -in dsa1.pem -pubout -out dsa1-public.pem
openssl pkey -in dsa2.pem -pubout -out dsa2-public.pem
```
Public keys:

[rsa1](rsa1-public.key) [rsa2](rsa2-public.key)

[esdc1](esdc1-public.key) [esdc2](esdc2-public.key)

[oldkey1](oldkey1-public.pem) [oldkey2](oldkey2-public.pem)

[dsa1](dsa1-public.pem) [dsa2](dsa2-public.pem)

New commands use PKCS#8 format and old ones use legacy format as seen by the difference between headings
```terminal
cat rsa1.key
-----BEGIN PRIVATE KEY-----

cat oldkey1.key
-----BEGIN RSA PRIVATE KEY-----
```
Base64 is used to represent key
### Task 1.3
```terminal
cat [FILE]
```
## Task 2
```terminal
openssl req -new -key rsa1.key -out rsa1.csr

openssl req -text -in rsa1.csr -noout
```
[rsa1.csr](rsa1.csr)


## Task 3

First I created 4 byte key with first two bytes predefined and two random bytes. Then I'm creating a new Blowfish cipher with the key and EAX-mode.
```python
from Crypto.Cipher import Blowfish
from struct import pack
from Crypto.Random import get_random_bytes

key = b'00' + get_random_bytes(2)
cipher = Blowfish.new(key, Blowfish.MODE_EAX)
plaintext = b'Takes about 20 seconds to brute force this open'

```
Padding is created
```python
bs = Blowfish.block_size
plen = bs - len(plaintext) % bs
padding = [plen]*plen
padding = pack('b'*plen, *padding)
```
Ciphertext is created. Nonce, MAC-tag and ciphertext are collected as they are needed for brute forcing. Key, plaintext and cipher object are deleted.
```python
nonce = cipher.nonce
ciphertext, tag = cipher.encrypt_and_digest(plaintext + padding)
del key, plaintext, cipher
```
Then all 2^16 possible keys are tried until we find the one that can be used to pass the verification. Finally plaintext is printed(with padding)
```python
for n in range(2**16):
    key = b'00' + n.to_bytes(2, 'little')
    cipher2 = Blowfish.new(key, Blowfish.MODE_EAX, nonce = nonce)
    try:
        plaintext = cipher2.decrypt_and_verify(ciphertext, tag)
        print("Authentic message:", plaintext)
        break
    except ValueError:
            pass
```
In this example I used EAX-mode so I can confirm the right key. Had i not used EAX, some other method would have been needed for verification(hash for example). EAX also requires nonce. To make it a bit simpler I'm also assuming that I know the key length.

## Task 4


### Introduction

Name of the application is Signal. Signal is a messaging application  for  android, iOS, macOS, Windows and Linux. It claims to have strong emphasis on security and is free for everyone to use.[1]

The reason I picked this application for review was  because  I've been using it. There have been claims that it is the best application for secure messaging. That’s why I wanted to take a peek under the hood to find out how they do things differently. 

The intended use of the application
Signal can be used to send personal and group messages. Messages can include files, pictures, sound and video. Voice and video calls can also be made. Signal is also open source application and it’s cryptography protocol(Signal Protocol) has been adopted by other applications too. For example Whatsapp uses Signal protocol since 2016[2]. Other notable protocol user is Facebook’s Messenger[3]. 


### Cryptography

All the messages and calls are end to end encrypted with the Signal Protocol. Algorithms used by the protocol are: Extended Triple Diffie-Hellman (X3DH) key agreement protocol, Double Ratchet algorithm, Curve25519, AES-256, and HMAC-SHA256. [2]

Messages are encrypted with 80-byte key. It consists of 32 bytes for an AES-256 , 32 bytes for a HMAC-SHA256 and 16 byte iv. For identity there is 32byte Curve25519 key. Curve25519 is also used for session keys. Root Key is 32-byte value that is used to create Chain keys . Chain Key is also a 32-byte value and it is used to create Message Keys. [2]


### Analysis

Level of security provided by the Signal application seems to be high. It uses secure algorithms and sufficiently long key sizes. I can’t find any gaps or discrepancies between different cryptographic primitives. It’s also very open about the cryptographic techniques it implements and it can and has been reviewed and analyzed by others. [3]


### References

[1] https://signal.org/

[2] “WhatsApp Encryption Overview: Technical White Paper”. 

[3] K. Cohn-Gordon, C. Cremers, B. Dowling, L. Garratt and D.  Stebila, "A Formal Security Analysis of the Signal Messaging Protocol," 2017 IEEE European Symposium on Security and Privacy (EuroS&P), Paris, France, 2017, pp. 451-466, doi: 10.1109/EuroSP.2017.27.
