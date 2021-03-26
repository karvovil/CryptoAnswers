from collections import Counter

def coincidenceRate(string):
    sumx = 0
    for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            sumx = sumx + (string.count(x)) * (string.count(x) - 1)
    k0 = sumx / ( len(string) * (len(string)-1 ))
    return k0

def shift(plain, shift):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    dictionary = str.maketrans(alphabet, shifted_alphabet)
    return plain.translate(dictionary)

def decrypt(encrypt_text, key): 
  orig_text = [] 
  for i in range(len(encrypt_text)): 
    x = (ord(encrypt_text[i]) - 
    ord(key[i%len(key)]) + 26) % 26
    x += ord('A') 
    orig_text.append(chr(x)) 
  return("" . join(orig_text)) 

def freqOrder(keyLength, cipher):
    frequencies = []
    for x in range(keyLength):
        counter = Counter(cipher[x::keyLength])
        sortedKeys = counter.most_common(len(counter))
        c=''
        for i in range(len(counter)):
            c =  c+  (sortedKeys[i])[0]
        frequencies.append(c)
    return(frequencies)


cipher = 'TRLSHAXRNSVKIENUFMEGRVDANEELHOFNSLUGIEFZVATAAGCIYAGIFADWUDHFYIFPOWVSPUMBKOTUOBYYNQWZYEEHBFCYCRZUKIPDZFFOYDBPZTPRBRVRFRBFYESLSXUAALBFIIAVWORLYBAAIAYGWYVNFLCZKHRVBANDRQFQMEYDHUFNFPCFZVNWSMIENVGQJSZHBFFFGKSBFLVWWORLNQRYFRNODAJIGLCZZNTRTOIYCWCSIACKMFYELOSMUOAHHARSXLTALRVQONZLVWMFFESISOKIIHZKRDQUSEJMNVGELRIHWXCAAFSOFNFWWFLTRVORRIYXFQFFBXFRZEYGWNVLVHJQKHNWWFUORVWORLYICDRCBPAGEIGBKUUERITAITGRRQMEYRDYFRRHTRVCGLJQDENQGFFRRVWEKMNVGELRIHWXCAAFSUGLRDRRFRNUSUEVRQHUFNBICGIDVVQUGLVQODPCHOHGIEGROFKEAGBAKOAOMFFPHCNXVSNQRYRTUEIFRLFRHAKHRVCOZEGDZUDPYLQMKIBQGAWOHUKAIK'


for keylength in range(1,13):
    rate=0
    for x in range(keylength):
        rate = rate + coincidenceRate(cipher[x::keylength] )
    print(keylength,' : ', rate/keylength)


keyLength = 6

print('   ')


for step in range(keyLength):
    biggestCount = 0
    biggestText = ''

    for x in range(26):
        text = shift( freqOrder(6,cipher)[step] ,x)
        count = 0
        eta = 'ETAION'
        for y in text[:6]:
            if y in eta:
                count = count +1

        if(count > biggestCount):
            biggestCount = count
            biggestX = x

    print(26-biggestX )
                
plain = decrypt(cipher, 'RANXOM')
print (plain)

plain = decrypt(cipher, 'RANDOM')
print( plain )

