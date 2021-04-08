import hashlib

cipherText = 0xa7896ad1b2f7da8d40b33d1438e04a839a88b5c9a97625fe5017a5e1fb542072595d804d5ad1a3af11ea7244a39d76cde1
plainText = int.from_bytes('Move the tables to the patio as soon as possible!'.encode('ascii'), 'big')
stream = cipherText^plainText

newPlain = int.from_bytes('Move the chairs to the house as soon as possible!'.encode('ascii'), 'big')

newCipher = stream^newPlain

print(hex(newCipher))



#print( hashlib.sha256(newCipher).hexdigest() )
