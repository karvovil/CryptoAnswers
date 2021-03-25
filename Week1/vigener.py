import binascii

def coincidenceRate(string):
    sumx = 0
    for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            sumx = sumx + (string.count(x)) * (string.count(x) - 1)
    k0 = sumx / ( len(string) * (len(string)-1 ))
    return k0

def shifter(plain, shift):
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

from collections import Counter



print('   ')
from difflib import SequenceMatcher
import Levenshtein


for x in range(26):
    text = shifter( freqOrder(12,cipher)[1] ,x)
    similarityRate = SequenceMatcher(None, text[:6], 'ETAION').ratio()
    lRate = Levenshtein.ratio(text[:6], 'ETAION')

 
    print(x,' ',text[:6],' ',lRate,' ',similarityRate)


a = freqOrder(12,cipher)
print ( a)
print( decrypt(cipher, 'JIRSMEJAT') )

#for x in range(6):
   # print (cipher[x::6])