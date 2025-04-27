# from Crypto.Util.number import long_to_bytes, bytes_to_long
# FLAG = b"khod l flag ila bghi FLAG = SECOPS{"+b"\x00"*21+b"}"

# modulus = 114194148014046069047177561921414220096046550618884143903108954448587080946107078663474628578411196689191838405386806197

# P = 1435885536835864899901057428193312502519570960784722161708476537457075911398448168488008991482817809707214361384095261823

# q = bytes_to_long(FLAG)//P
# print(q)
# for i in range(100):
#     if b"SECOPS" in long_to_bytes(P*(q+i)+ modulus):
#         print(long_to_bytes(P*(q+i)+ modulus))
#         break

from Crypto.Util.number import long_to_bytes

# Given values
P = 1435885536835864899901057428193312502519570960784722161708476537457075911398448168488008991482817809707214361384095261823
r = 114194148014046069047177561921414220096046550618884143903108954448587080946107078663474628578411196689191838405386806197

# The known part of the message before the flag
prefix = b"khod l flag ila bghi FLAG = SECOPS{"
# The known part after the flag (just '}')
suffix = b"}"

# The total length of the original message is 57 bytes
# Length of prefix is 35 bytes, suffix is 1 byte, so the flag part is 21 bytes
flag_length = 21

# We need to find k such that FLAG = k * P + r, and when converted back to bytes,
# it starts with the prefix and ends with the suffix, with the flag in between.

# Let's compute the numeric value of the prefix
prefix_long = int.from_bytes(prefix, 'big')
# The prefix is 35 bytes, and the total message is 57 bytes, so the flag is 21 bytes, then '}'
# So the structure is: prefix (35 bytes) + flag (21 bytes) + suffix (1 byte)
# The numeric representation is:
# FLAG = prefix_long * (2 ** (8 * (flag_length + 1))) + flag_long * (2 ** 8) + suffix_long
# Where suffix_long is ord('}') = 125

# We can rearrange FLAG = k * P + r to solve for flag_long:
# k * P + r = prefix_long * (2 ** (8 * 22)) + flag_long * 256 + 125
# So:
# flag_long = (k * P + r - prefix_long * (2 ** 176) - 125) // 256
# We need flag_long to be a 21-byte integer (between 0 and 2**(21*8) - 1)

# Let's compute 2**176 (since 22 bytes = 176 bits)
power_176 = 2 ** (8 * 22)

# Now, we can iterate over possible k values to find the correct flag_long
# Since FLAG is 57 bytes (456 bits), and P is ~370 bits, k should be around 2^(456-370) = 2^86
# But iterating over all possible k is infeasible, so we need a smarter way.

# Alternatively, since the prefix is fixed, we can compute the expected high bits of FLAG
# and find k such that k * P + r has those high bits.

# Let's compute the minimal k where k * P + r >= prefix_long * power_176
# We can estimate k as:
k_min = (prefix_long * power_176) // P
# And then check k around this value to find the correct flag_long

# Let's try k around k_min
for delta in range(-10, 10):
    k = k_min + delta
    FLAG = k * P + r
    # Now, extract flag_long
    remainder = FLAG - prefix_long * power_176 - 125
    if remainder < 0:
        continue
    flag_long = remainder // 256
    if remainder % 256 != 0:
        continue  # Not divisible by 256, so invalid
    # Check if flag_long is 21 bytes
    if flag_long.bit_length() > 21 * 8:
        continue
    # Convert flag_long to bytes
    flag_bytes = long_to_bytes(flag_long)
    # Ensure it's 21 bytes (pad with zeros if necessary)
    flag_bytes = flag_bytes.rjust(21, b'\x00')
    # Now, reconstruct the full message
    full_message = prefix + flag_bytes + suffix
    # Check if the length is 57 bytes
    if len(full_message) == 57:
        print(f"Found potential flag: SECOPS{{{flag_bytes.decode()}}}")
        break
else:
    print("No valid flag found in the tested range.")