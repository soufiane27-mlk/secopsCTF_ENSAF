from pwn import*

io = remote("ensafacademia.ddns.net",5011)
maxi = 2500
mini = 0 

def calculate_moy(max_,min_):
    return (max_+min_)//2

i=0
while True:
    moy = calculate_moy(maxi, mini)
    io.sendlineafter("guess the number:", str(moy))
    io.recvline()
    line = io.recvline().decode()
    if "too big" in line :
        maxi = moy
    elif "too small" in line:
        mini = moy
    else:
        print(io.recvall())
        exit()
    i+=1
