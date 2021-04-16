import requests
from base64 import b64decode, b64encode
from hashlib import sha256

s = requests.Session()
s.post('http://0.0.0.0:5000/login', data = {'username':'cryptonator','password':'cryptonator'})

cookie = s.cookies['auth']
b64_data, b64_sig = cookie.split('.')
data = b64decode(b64_data)
sig = b64decode(b64_sig)

print(data.decode())
print( sig.hex() )


newdata = b'username=cryptonator;secret=407c691f79d096412bae2b133e2d053414167042b55928f34a2c15c84210d297;\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03H;username=admin;secret=6b337775fce2301772f36e05a10ed9822033a7496520cf24ebe13ed324262c99;'
newsig = bytes.fromhex('a80a460353ed983ff879526b2587f35e3762769e7381129096519a9b3ed5b7be')
b64sig = b64encode(newsig).decode()
b64data = b64encode(newdata).decode()

newAuth = b64data +'.'+ b64sig
cookies = dict(auth = newAuth)

s2  = requests.Session()
r = s2.get('http://0.0.0.0:5000/admin/top-secret', cookies = cookies)
print(r.text)