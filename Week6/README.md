# Answer template for Crypto course, week 6


## Task 1

### Task 1.1
Here's the message: [message.txt](message.txt)

Private key generation [week6.key](week6.key)
```console
openssl genpkey -out week6.key -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -aes-128-cbc
```

### Task 1.2
public key generation [week6public.key](week6public.key)
```console
openssl pkey -in week6.key -pubout -out week6public.key
```

Encryption [encrypted.txt](encrypted.txt)
```console
openssl rsautl -encrypt -pubin -inkey week6public.key -in message.txt -out encrypted.txt
```

Signature [signature.txt](signature.txt)
```console
openssl dgst -sha256 -sign week6.key -out signature.txt message.txt
```






## Task 2

### Task 2.1
Start by reading messages and generating hashes from them
```python
hashes = []
f = open('files/messages.txt')
messagelines = f.read().splitlines()
for message in messagelines:
    hashes.append(SHA1.new(message.encode())) 
```
Then read the keys and signatures.
```python
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
```
Then loop over everything and print the message and name of the keyfile and sinature file when signature matches.
```python
for h in range(20):
    for k in range(5):
        for s in range(20):
            try:
                pkcs1_15.new(keys[k]).verify(hashes[h], sigs[s])
                print(h+1, ' '+ keyfiles[k] +'  '+ sigfiles[s])
            except (ValueError):
                pass
```

Here are the matches. 
```console
1  public_key1.pem  signature18.sign
1  public_key5.pem  signature17.sign
2  public_key1.pem  signature2.sign
3  public_key1.pem  signature1.sign
4  public_key5.pem  signature14.sign
7  public_key3.pem  signature8.sign
8  public_key1.pem  signature3.sign
8  public_key2.pem  signature4.sign
9  public_key2.pem  signature6.sign
11  public_key3.pem  signature9.sign
12  public_key3.pem  signature7.sign
13  public_key2.pem  signature5.sign
15  public_key3.pem  signature10.sign
16  public_key3.pem  signature11.sign
17  public_key4.pem  signature12.sign
18  public_key4.pem  signature13.sign
19  public_key2.pem  signature20.sign
19  public_key5.pem  signature15.sign
20  public_key2.pem  signature19.sign
20  public_key5.pem  signature16.sign
```
### Task 2.2
Textbook RSA seems to have many many vulnerabilities. Here are four of them:

From a signature it is possible to calculate such a message that the verification will pass.

Signatures can be combined to calculate a new signature for a new message.

Let's say we have message m we don't have signature for. If we know signature for mr^e then it is possible to calculate signature for m.(As in the next task)

if 0^d mod n = 0, 1^d mod n = 1, and (n – 1)^d mod n = n – 1, where d is the private exponent and n is the modulus, then signature of 0, 1, or n – 1, can be forged

## Task 3
### Task 3.1
Lets start by getting the public key and defining the message we want the signature for 
```python
file = open('files/alice.pub', 'r')
pubkey = RSA.import_key( file.read() ) 

evilmessage = int.from_bytes(b'_p', "big")
```
Then we find a suitable r so that the new message mr^e mod n will get signed by alice. 
```python
for r in range(99999999999):
    newint = pow(r, pubkey.e, pubkey.n)*evilmessage % pubkey.n
    newbytes = newint.to_bytes((newint.bit_length() + 7) // 8,'big')
    if newbytes[:2] == b'_n' :
        break
```
Then message is written to a file and passed to alice who signs it
```python
with open("files/file1", "wb") as file:
    file.write(newbytes)
    file.close()
    
result = subprocess.run(["files/./alice" ,'-j',"-f", 'files/file1'], capture_output=True) 
dick = json.loads(result.stdout.decode('ascii'))
sig = int(dick['signature'], 16)
```
Now the signature for the message "_p" should be sig/r mod n. Let's calculate it by multiplying signature with modular inverse of r. 
```python
evilsig = sig * pow(r,-1,pubkey.n)

print(hex(newint))
print(hex(sig))
```
Forged message and signature of "_p":
```console
0x5f6e82b7efab608951c82dda80fd2b46a6e2c54b737e2206f89d053a834d333e161b85ecc6a8624d7e019fb7ad68aae931bff35d64cc1c406dd8e10a0d2b23def4b706fb5d258e3a3bfcc9dfa9a03e1c96a2ab5dddeef26eae18d68c33a3b304e074c9ddc5925470d6bef808f13eab833c08d57111b8feab5f6578fa5c9bf9ad06d67d303c350301d55d20837e2b7c196cc3a296619981585597cc1cc32716c2b4f7b41900438e60ac691e97fab14ca4261945d64af5f1ababa990864b336d276d65641febaacc087c5bfadeaf3e967301fc85e47a36c9f8f974870d209600ec7cc4bea4b14b6c953645a4c2a5c2928991b5460450284ca259875f35fd3b8228154c702a46ab91e6530a954cfe3a89b82712b715f285fe1c7600a744fdef6a01295b82718bf1e8fc3e05b948cb58d80155a9292a7332387164e818deb4ce56f5d65144a596768ef3be155719afcae7155dd559de3229dd5161b67cd61fe7655c83c81001122ae8eab9aac3e1cf92fdd79ec9d409acc316580b667bbc5dfefe72b5f9884bfac55cc6a101f16c001bef13d5a7a25eb127c42fadecfaf45bc90a76c40a3aa149db182f4163dda2700fad5208c941567282362330bb345884fa2bb5362abafe6e5702352bcf3707a927f570cc3fd8826281c2c86942578f8b3c832f130a1b5eb3644ce147032956261e4e01aa15e61732425833dcd9136d18f6257a
0x1ab2620aca334e2140aafe254d754cc4598027d475ef324cee40ff2dcede0db2512c6bc1fb20a35e005c4c912fff367c74aa485c4d489e81ce1c4c697a499948a69441c4d768fca8da4cc3f539ab9f3d621ff5cbc56e441f5dcc69c8b0680aaf7436bdeab4235c5851d5b8728e0d242f074fd53e811ff6f88e8f76ed840e7baf363dba344b35638be4fee0e15b5bf287bc8ccd8356d5515c574c65e86faaeee9508fd3bc255d228b2384de213ad5998e68286955e55a98d868d49eeebff070772afe6dca5687d5f01b8c4114aa82d90a55e32c073b78507e7f83a29b76af7ccead855e02850a744a18daa4d3f8f536b33f3a0814c8e101c5d1db338cb2b3fa2d0d51bb641d1e2af22d3cada6e92581b0a6d17dda69b71da25275500f3bf8e416b549d1bc4f52e449867ba320431fe73830ef515f26ee915219dc342e23247748b9c615737864df07c22676763fe2e82e24dde97b87f83fd89cf18257a3957c7d36df3e02fb0ed27abc55e5b525b446445205fa3e0e066c1f7f963393dfc1df5294eef2c15ec4034abf39885afbbfa71f414e3046b9faa2b5cf86116c13be7890f74ad4d242a01400d091ad5972af149972552229520fe33d0c4c57373df84a069c6b386af446ef68ee2e9ad5046691862c91c8b5630056e0f27c400539eccb230c395200a6ad09a3a54d8a7635a2998d356c38c36f914357f30603cf9320108f
```

### Task 3.2
Difficulty of the process grows exponentially with every bit of real data we need to provide to alice. If the difficulty of our current situation would be presented as 2^16 then the difficulty of 3 byte situation would be 2^24.

## Task 4
### Task 4.1
My cryptosystem is based on factoring. Humans have been factoring integers for few thousand years and they haven't still found easy way to do it so it must be hard. In other words: there are no known algorithms that can do it in polynomial time.

For our key we generate positive integers p, s and n so that p*s=1 mod n. p should be much much bigger.

p and n are our public key and encryption is done by multiplying message with p mod n. s is private key and decryption is done by multiplying with e mod n. signing is done by multiplying message with e so it can be verifired by multiplying with d.


### Task 4.2
```python
def newkey()
    find numbers p,s,n so that p*s=1 mod n
    p should be much bigger than s
    add some randomness to process 
    return p,s,n

def encrypt(p,m,n):
    return p*m%n

def decrypt(s,m,n):
    return s*m%n

def sign(s,m,n):
    return s*m%n

def validate(p,m,n):
    return p*m%n
```
To multiply two l long ints with each other I would need ll operations to get the product. At least the way I have done it since elementary school. So O(l^2)

### Task 4.2

Obvious problem with my system is that it's not actually based on problem of factoring integers. Actual problem is finding modular multiplicative inverse, which is not such a hard problem( O(log n) ). So practical attack would be to bruteforce s from p and n to break whole system.

It can be a problem that same text encrypted twice will result both times to same ciphertext.

If attacker gets hold of multiple ciphertexts, they can be combined to forge a new ciphertext. c1c2 = sm1sm2 = s(m1m2) and also c1+c2 = sm1+sm2 = s(m1+m2)


### Task 4.3

Modular inverse results are dealing mostly with lecture materials and effective methods to finding modular inverse. This is not surprising as modular inverse calculations are needed in many modern cryptosystems. Rather than these systems depending on complexity of finding modular inversion, they depend on feasibility of finding them.

Factoring integers search results to similar kind of materials for similar reasons. Maybe even more research papers as we are now interested also about breaking systems by finding factors.

### References


Berners-Lee et. al.(1989). *interweb.*   Retrieved 29.4.2021

Course book