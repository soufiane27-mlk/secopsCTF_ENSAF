# 🛡️ Challenge Writeup — baby RSA
---

## 📜 Challenge Description

You need P and Q to find the privat key (d). what if a give you some thing else : a leak

> **Author:** s0ufm3l
---

## 📜 Challenge Description

In this RSA-based challenge, we are given:
- `n` (the RSA modulus)
- `enc` (the encrypted flag)
- `leak` (a weird value related to the prime `p`)

The goal is to recover the flag.

---

## 📥 Given

The server/code provides:
- eak = A*(p^2) + B*p + C 
- n = p * q 
- e = 0x10001
- enc = pow(FLAG, e, n) 

where:
- `A = bytes_to_long(b"SEC")`
- `B = bytes_to_long(b"OPS")`
- `C = random 24-bit number (small!)`

---
🧠 Solution
    We can brute-force all possible values of C (from 0 to 2**24), and for each candidate C, solve the quadratic equation: 
    A * p² + B * p + C = leak
    to find a possible prime p.
    If the equation has an integer solution p such that n % p == 0, then we have correctly found p.
    After recovering p, we can compute:

    q = n // p
    phi = (p - 1) * (q - 1)
    d = inverse(e, phi)

    Finally, we can decrypt the ciphertext enc and recover the flag.