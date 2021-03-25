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

### Task 2.x

## Task x
