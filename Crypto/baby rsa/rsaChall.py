from Crypto.Util.number import bytes_to_long, getPrime
from secrets import randbits

FLAG = b"REDACTED"

p = getPrime(1024)
q = getPrime(1024)
n = p*q
e = 0x10001
enc = pow(bytes_to_long(FLAG),e,n)

A = bytes_to_long(b"SEC")
B = bytes_to_long(b"OPS")
C = randbits(24)

leak = A*(p**2) + B*p + C

print(f"{leak = }")
print(f"{n = }")
print(f"{enc = }")

