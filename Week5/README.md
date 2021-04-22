# Answer template for Crypto course, week 5

Add your work into this template and make every task from the instruction repository to get full points. If screenshots are required, add them into `img` folder, and reference as Markdown allows. If your own code is required, you can add it into this document by using `code blocks`. You can create own `src` folder for all code, in case there is a plenty of it. In general, you have freedom to express your work as you please.

**Remember to mention/reference all your attachments in this main document!**

You should remove all of the examples and instructions from this document.

## Task 1

### Task 1.1

Here's the encryption part. AES with CCM mode is used to produce ciphertext and 4 byte mac(shortest allowed by PyCryptodome). Key is random 16 byte value and plaintext is equally random 4 byte value. plaintext and mactag are printed in hexadecimal.
```python
key = get_random_bytes(16)
data1 = get_random_bytes(4)
cipher1 = AES.new(key, AES.MODE_CCM, mac_len = 4)

nonce = cipher1.nonce
ciphertext1, tag1 = cipher1.encrypt_and_digest(data1)
print('data1: ' + data1.hex())
print('tag1: ' + tag1.hex())
```
Then we start brute forcing a message by converting counter d to bytes. Same nonce and key are used for mac generation. Produced mac is compared to previosly generated mac. Time is taken and printed in seconds. 4 bytes would take too much time so I'm only checking for partial match.
```python
start = time.time()
for d in range(2**24):
    data2 = d.to_bytes(24, byteorder='big')
    cipher2 = AES.new(key, AES.MODE_CCM, mac_len = 4, nonce=nonce)
    ciphertext2, tag2 = cipher2.encrypt_and_digest(data2)
    if tag2[:3] == tag1[:3]:
        end = time.time()
        break

print('data2: ' + data2.hex())
print('tag2: ' + tag2.hex())
print('time: ',end-start)
```
Output:
```console
data1: 31d1de9d
tag1: 157b2c9d
data2: 0085a4a8
tag2: 157b2c7e
time:  962.6760518550873
```

## Task 2

Start by reading the ciphertext and encoding.
```python
with open("ciphertext", "rb") as file:
    cipherbinary = file.read()
file.close() 
ciphertext = b64encode(cipherbinary).decode()
```
Next we define the method for timing the execution of the verification. I'm timing 20 consecutive verifications as this is when I start getting reliable results. If the correct mac is found, results are printed and execution terminated.
```python
def mactime(mac):
    data = {
    "sender": "Bob",
    "receiver": "Alice",
    "data": ciphertext,
    "tag": mac 
    }
    with open("data.json", "w") as f:
        json.dump(data, f)
    f.close()

    start = time()
    for _ in range(20):
        result = subprocess.run(["./authenticator" ,"-f", "data.json"], capture_output=True)
        if(result.returncode == 0):
            print(result)
            quit()
    end = time()

    return(end-start)
```
With findslowest method I'm finding the byte that takes longest to execute verification with. Already found bytes are passed as argument. Method calls itself with already found bytes + newfound byte.

```python
def findslowest(verifiedBytes):
    slowestTime = 0
    slowestByte = ''
    for n in range(256):
        testByte = n.to_bytes(1, byteorder='big').hex()
        testTime = mactime( verifiedBytes + testByte )
        if testTime > slowestTime:
            slowestByte = testByte
            slowestTime = testTime   
    findslowest(verifiedBytes + slowestByte)
```
Finally we call findslowest with empty string
```python
findslowest('')
```

```console
CompletedProcess(args=['./authenticator', '-f', 'data.json'], returncode=0, stdout=b'\nBob!?? I just send them for you, did you miss them? \nBut here we go, as we are investing in ENCRYPTO, the future super cryptocurrency provider, here are the defails:\nStreet: 4883  Lousy Drive\nCity: Cryptoville\nState: TX\nState Full: Texas\nZip Code: 39349\n\n', stderr=b'')
```
## Task 3
Don't really know. I've tried compiling lists of random authentication keys raised to multiple powers in GF(2^128). Can't find anything.
Neither am I able to produce a forgery.

## Task 4
First we define simple validator for the first situation.
```python
def validate(key, message):
    data = message[:-32]
    tag = message[-16:]
    iv = message[-32:-16]
    cipher = AES.new(key, AES.MODE_CBC, iv = iv)
    ct = cipher.encrypt(pad(data, AES.block_size))

    validtag = ct[-16:]
    if validtag == tag:
        print('Valid!')
```
Random key and random iv are used for encryption. Message is constructed as specified
```python
key = get_random_bytes(16)
data = b'from=alice;to=bob=amount=40;'
iv = get_random_bytes(16)

cipher = AES.new(key, AES.MODE_CBC, iv = iv)
ct = cipher.encrypt(pad(data, AES.block_size))
tag = ct[-16:]
message = data+iv+tag 
```
This is a very simple example as we are only changing one byte but every one of first 16 bytes can be changed same way.
In this demonstration middleman gets the message and creates a new message with first letter changed from f to w. 
```python
data = message[:-32]
iv = message[-32:-16]
tag = message[-16:]
newdata = b'wrom=alice;to=bob=amount=40;'
```
Then we need to change first byte of iv so it will produce same tag with changed data. newiv^newdata == iv^data  should hold true for us to achieve same tag. 
```python
newivbyte = iv[0]^data[0]^newdata[0]
newiv = newivbyte.to_bytes(1, 'big') + iv[1:]
newmessage = newdata+newiv+tag
```
After constructing the message with the new data and new iv it's send to the validator.
```python
validate(key,newmessage)
```
Validator validates. First block can be changed anyway we want and still keep the tag same as long as we also modify iv. Iv size is same as block size and also the amount of bytes we are able to change.
```console
Valid!
```

In the next case we stop using encryption iv for mac generation and instead use all zeros iv.
```python
zeroiv = bytes(16)
```
New validator is defined to validate mac:s using zero iv.
```python
def validate0(key, data, tag):
    cipher = AES.new(key, AES.MODE_CBC, iv = zeroiv)
    ct = cipher.encrypt(data)
    validtag = ct[-16:]
    if validtag == tag:
        print('Valid!')
```

Here random key is generated and some messages are defined and padded. 
```python
key = get_random_bytes(16)
a =  pad(b'this is dataaaaaaaaaaaaaaaaaaaa', 16)
b =  pad(b'There might be even more bytes here', 16)
ab = a+b

```
And correspoding ciphertexts and mac tags:
```python
cipher = AES.new(key, AES.MODE_CBC, iv = zeroiv)
ct1 = cipher.encrypt(a)
atag = ct1[-16:]

cipher = AES.new(key, AES.MODE_CBC, iv = zeroiv)
ct2 = cipher.encrypt(b)
btag = ct2[-16:]

cipher = AES.new(key, AES.MODE_CBC, iv = zeroiv)
ct3 = cipher.encrypt(ab)
abtag = ct3[-16:]
```
If we know two messages and corresponding mac tags It's possible to generate message that will validate with one of the macs. Here we are calculating a new message which will validate with b:s mac. It's a || (a:s tag xorred with last block of b) || all the other blocks of b. 
```python
newdata1 = a + strxor(atag,b[:16]) + b[16:]
```
Same method can be used with any combination of known messages and once we create new message, it can be combined with another message to create jet another message.  Here we are using ab and a to create new message:
```python
newdata2 = ab + strxor(abtag,a[:16]) + a[16:]
```
Both are valid. 
```console
Valid!
Valid!
```

If the receiver uses same key for encryption and authentication, mac becomes almost useless. In this case mac is always the last block of ciphertext so as long as we dont change last ciphertext block authentication passes. Everything else in the ciphertext can be modified.