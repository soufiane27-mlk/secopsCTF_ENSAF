import random 

FLAG = "SECOPS{B1NaRY_S34RCH_13_F4ST3R}"

WIDTH = 500

theSide = random.randint(1000,2000)
theNumber = random.randrange(theSide, theSide+WIDTH)

print("You have 10s to find the number !!!")
n=0
while n<12:
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
    n+=1
print("You only have 12 chances to find the number.")