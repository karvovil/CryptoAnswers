plain = int.from_bytes('Hi Kimmo'.encode('ascii'), 'big')
cipher = 0x69155f4e201cad61
key = plain^cipher
print( hex(key) )

plain = int.from_bytes('No Rauli'.encode('ascii'), 'big')
cipher = key^plain
print( hex(cipher) )

plain = int.from_bytes('MyChoice'.encode('ascii'), 'big')
cipher = key^plain
print( hex(cipher) )


print ( bin(key) )

