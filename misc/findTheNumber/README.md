# 🛡️ Challenge Writeup — Binary Search Challenge

---

## 📜 Challenge Description

Use a binary-search script to find the secret number and get the flag.

> **Author:** s0ufm3l

---

## 🔗 Connection Details

- Host: `nc ensafacademia.ddns.net 5011`
- Provided file: `search.py`

---

## 📥 Code Analysis

The challenge script (`search.py`) works as follows:

```python
import random

FLAG = "SECOPS{B1NaRY_S34RCH_13_F4ST3R}"

WIDTH = 500

theSide = random.randint(1000, 2000)
theNumber = random.randrange(theSide, theSide + WIDTH)

print("You have 10s to find the number !!!")
n = 0
while n < 12:
    print(f"chances left : {12-n}")
    try:
        guess = int(input("guess the number: "))
    except Exception:
        print("Please enter a number !")
        exit(1)
    if guess > theNumber:
        print("too big")
    elif guess < theNumber:
        print("too small")
    else:
        print("Wow! you found the right Number.")
        print(f"Here is you flag: {FLAG}")
        exit(1)
    n += 1

print("You only have 12 chances to find the number.")
```
## 🧠 Key Observations

    A random number theNumber is generated between a range of 1000~2000 + 500.

    You have 12 tries to guess it.

    After each guess, you are told if your guess was too big or too small.

    If you find the number within 12 tries, you win and receive the flag.

🧠 Solution Strategy

This is a classic Binary Search problem!

    You can cut the search space in half after each guess.

    Each time you guess the middle of the current range:

        If the guess is too big, you adjust the maximum bound.

        If the guess is too small, you adjust the minimum bound.

🔵 With binary search, you can find the number efficiently within 12 tries max.

## 🚀 Exploit Script

We can automate the guessing using a simple script with binary search logic.

Here’s the working solve.py:

```python
from pwn import *

io = remote("ensafacademia.ddns.net", 5011)

maxi = 2500
mini = 0 

def calculate_moy(max_, min_):
    return (max_ + min_) // 2

while True:
    moy = calculate_moy(maxi, mini)
    io.sendlineafter("guess the number:", str(moy))
    io.recvline()
    line = io.recvline().decode()
    if "too big" in line:
        maxi = moy
    elif "too small" in line:
        mini = moy
    else:
        print(io.recvall())
        exit()
```