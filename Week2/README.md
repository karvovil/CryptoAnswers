# Answer template for Crypto course, week 2
## Task 1

### Task 1.1
Private keys are generated:
```console
time openssl genpkey -out rsa1.key -algorithm RSA -pkeyopt rsa_keygen_bits:2048 
time openssl genpkey -out rsa2.key -algorithm RSA -pkeyopt rsa_keygen_bits:8192

time openssl genpkey -out esdc1.key -algorithm EC  -pkeyopt ec_paramgen_curve:P-256 
time openssl genpkey -out esdc2.key -algorithm EC  -pkeyopt ec_paramgen_curve:P-384 

time openssl genrsa -out oldkey1.pem 2048
time openssl genrsa -out oldkey2.pem 4096

time openssl dsaparam -noout -out dsa1.pem -genkey 1024
time openssl dsaparam -noout -out dsa2.pem -genkey 4096
```
Correspondning times:
```terminal
user	0m0.298s
user	0m8.026s

user	0m0.004s
user	0m0.005s

user	0m0.115s
user	0m0.558s

user	0m0.042s
user	0m2.271s
```
Public key generation:
```terminal
openssl pkey -in rsa1.key -pubout -out rsa1-public.key
openssl pkey -in rsa2.key -pubout -out rsa2-public.key

openssl pkey -in esdc1.key -pubout -out esdc1-public.key
openssl pkey -in esdc2.key -pubout -out esdc2-public.key

openssl pkey -in oldkey1.pem -pubout -out oldkey1-public.pem
openssl pkey -in oldkey2.pem -pubout -out oldkey2-public.pem

openssl pkey -in dsa1.pem -pubout -out dsa1-public.pem
openssl pkey -in dsa2.pem -pubout -out dsa2-public.pem
```
### Task 1.2
New commands use PKCS#8 format and old ones use legacy format as seen by the difference between headings
```terminal
cat rsa1.key
-----BEGIN PRIVATE KEY-----

cat oldkey1.key
-----BEGIN RSA PRIVATE KEY-----
```
Base64 is used to represent key
### Task 1.3
```terminal
cat [FILE]
```
Add your work into this template and make every task from the instruction repository to get full points. If screenshots are required, add them into `img` folder, and reference as Markdown allows. If your own code is required, you can add it into this document by using `code blocks`. You can create own `src` folder for all code, in case there is a plenty of it. In general, you have freedom to express your work as you please.

**Remember to mention/reference all your attachments in this main document!**

You should remove all of the examples and instructions from this document.



Example code block for Python highlighting:

```python
# In Python syntax
print("Hello, World!")
```

### Task 1.x

Example command in console format:
```console
$ for j in {1..9};do echo "Hello $j";done
```

## Task 2

### Task 2.1

Example image from the other directory. Create own in this directory for the images if they are needed.

![Example image](../.img/python_screenshot.png)

### Task 2.x

## Task x
