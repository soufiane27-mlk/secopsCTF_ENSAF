# 🛡️ Challenge Writeup — pyjail_revenge

---

## 📜 Challenge Description

You have two portals — only one leads to the treasure.  
(Find the flag!)

> **Author:** s0ufm3l

---

## 🔗 Connection Details

- Host: `nc ensafacademia.ddns.net 5004`
- Provided file: `pyjail_revenge.py`

---

## 📥 Code Analysis

We are given a Python Jail script that behaves differently based on our input.

First, the user input is taken:

```python
code = input("gol chno bghiti yalah > ")
```
The program checks if all characters are printable ASCII:

```python
rak_dayz = all([(char in string.printable) for char in code])
```
If true, it proceeds to further checks:

1. Input with only lowercase letters and spaces
If the input contains only lowercase letters and spaces, it is executed using exec():
```python
sayn_sayn_nchof = all([(char in string.ascii_lowercase + " ") for char in code])
if sayn_sayn_nchof:
    exec(code)
    exit(sayn_sayn_nchof)
```
✅ Here is our main exploitation opportunity!
We can execute arbitrary Python code.

2. Input with only numbers and punctuation

If the input contains only digits and punctuation, it is passed to eval():
```python
elif all([(char in string.punctuation + string.digits) for char in code]):
    print("wach bghiti t7ssab chi 7aja ??")
    value = eval(code, {"__builtins__": None})
    print(f"{code} = {value}")
```
But:

    __builtins__ is removed, making dangerous operations unavailable.

    Only simple math-like expressions are allowed.

❌ No way to execute commands here.

## 🧠 Exploitation Strategy

Our only real option is to use the exec() branch.

Now, notice this line after the exec():

```python
exit(sayn_sayn_nchof)
```

    After executing our code, it calls exit().

    If we can redefine exit to something else, we can gain control!

The Trick: Hijack exit to code.interact

In Python, code.interact() opens an interactive python interpreter.

We can:
```python
from code import code as exit
```
    it will launch a Python interactive shell!

Then inside the shell:

    We can import modules like os

    Execute system commands

    Read the flag!