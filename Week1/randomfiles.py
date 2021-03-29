import os
import random
import secrets


f = open("rand1", "wb")
f.write(os.urandom(161000000))
f.close()
    
f = open("rand2", "wb")
f.write(secrets.token_bytes(161000000))
f.close()