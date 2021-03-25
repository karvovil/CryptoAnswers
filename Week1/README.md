# Week1 answers Ville Karvonen

## Task 1

Key is simply produced by xor operation between ciphertext and plaintext
```python
plain = int.from_bytes('Hi Kimmo'.encode('ascii'), 'big')
cipher = 0x69155f4e201cad61

key = plain^cipher
```
key: 0x217c7f054971c00e


### Task 1.1

Ciphertext is produced by xor operation on plaintext and key

```python
plain = int.from_bytes('No Rauli'.encode('ascii'), 'big')
cipher = key^plain

key = plain^cipher
```
ciphertext: 0x6f135f572804ac67

### Task 1.2

Again, xor plaintext with key
Ciphertext from 'MyChoice': 0x6c053c6d2618a36b

If plaintext is longer than key, then beginning of the message wont be encrypted. This is because beginning of key is filled with zeroes until plaintext length is achieved. This makes xor operation possible but leaves beginning of the message unencrypted.


### Task 1.3

```python
print ( bin(key) )
#0b10000101111100011111110000010101001001011100011100000000001110
```
If we are able to intercept ciphertext, it can be altered without receivers knowledge. Furthermore, If we know part of the plaintext, we can alter that part of the ciphertext in a meaningful way.
## Task 2

### Task 2.1
Let's start by finding the key length. For this I'm defining method coincidenceRate that calculates index of coincidence for a string

```python
def coincidenceRate(string):
    sumx = 0
    for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            sumx = sumx + (string.count(x)) * (string.count(x) - 1)
    k0 = sumx / ( len(string) * (len(string)-1 ))
    return k0
```
Then I'll check the index of coincidence for different key lengths
```python
for keylength in range(1,13):
    rate=0
    for x in range(keylength):
        rate = rate + coincidenceRate(cipher[x::keylength] )
    print(keylength,' : ', rate/keylength)

```

Which produces following:
```terminal
1  :  0.04432011803030402
2  :  0.047323811018678386
3  :  0.05382321023803561
4  :  0.04643761981845815
5  :  0.04305059020655351
6  :  0.06756349463221833
7  :  0.043816942551119765
8  :  0.0464011691633175
9  :  0.05241201010635173
10  :  0.04512506012506012
11  :  0.044707337480446724
12  :  0.0666289786548806
```
Looks like 6 is the most propable key length as index of coincidence for english language is around 0,067
### Task 2.x

## Task x
