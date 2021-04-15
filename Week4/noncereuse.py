import statistics
from statistics import mode
import binascii

def solveX(crap):
    alphabet = bytes('qwertyuiopasdfghjklzxcvbnm ', 'ascii')
    possiblevalue = []
    for x in alphabet:
        for y in crap:
            possiblevalue.append(y^x)
    return mode(possiblevalue)


with open("task3_messages.txt", "r") as file:
    lines = file.read().splitlines()
file.close() 

cipherInts = []
for x in range(10):
    cipherInts.append( list(binascii.unhexlify(lines[x])))

baskets = []
for n in range (50):
    singleBasket = []
    for intList in cipherInts:
        singleBasket.append( intList[n] )
    baskets.append(singleBasket)

stream = []
for x in range (50):
    stream.append( solveX(baskets[x]) )

plain = []
for cipherLine in cipherInts:
    for n in range (50):
        plain.append( stream[n]^cipherLine[n] )

plainAscii = ''.join(chr(i) for i in plain)
print (plainAscii)


stream[16] = cipherInts[0][16]^ord('c')
stream[19] = cipherInts[0][19]^ord('d')
stream[28] = cipherInts[0][28]^ord('a')
stream[38] = cipherInts[0][38]^ord('t')
stream[40] = cipherInts[0][40]^ord('e')
stream[42] = cipherInts[0][42]^ord('c')
stream[49] = cipherInts[0][49]^ord('w')

plain = []
for cipherLine in cipherInts:
    for x in range (50):
        plain.append( stream[x]^cipherLine[x] )

plainAscii = ''.join(chr(i) for i in plain)
print (plainAscii)

                       