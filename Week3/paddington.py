import subprocess
from Crypto.Random import get_random_bytes

def isValid(dada):
    with open("newfile", "wb") as file:
        file.write(dada)
        file.close()
        result = subprocess.run(["./decryptor" ,"-f", "newfile"], capture_output=True)
        if(result.returncode == 0):
            return True     
        else:    
            return False

def shiftUp(block, n):
    pads = bytearray()
    for x in range(n):
        newByte = block[(-1-x)]^n^(n+1) 
        pads.insert(0, newByte )  
        newBlock = block[:16-n] + pads  
    return newBlock

def solveBlock(block1, block2):
    plain = ''
    for n in range(1,17):
        for x in range(256):
            testByte = x.to_bytes(1, 'little')
            testData = block1[:16-n] + testByte + block1[17-n:] + block2  
            if( isValid(testData) ):
                plain += chr( n^x^block1[-n] )
                block1 = testData[:16]
                block1 = shiftUp(block1, n)           
            else:    
                pass
    return plain[::-1]


with open("ciphertext", "rb") as file:
    data = file.read()
file.close() 

plainText=''
for x in range(0, 97, 16):
    block1 = data[x:x+16]
    block2 = data[x+16:x+32]
    plainText += solveBlock(block1, block2)
    
print(repr(plainText))


