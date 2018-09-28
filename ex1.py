import os
import binascii

a = os.urandom(15)
b = binascii.hexlify(a)
print(a, type(a))
print(b, type(b), int(b, 10))