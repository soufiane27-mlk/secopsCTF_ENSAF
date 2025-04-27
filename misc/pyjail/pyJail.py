import string
while True:
    number = input('>> ')
    if number:
        number+="+"
    print(eval(f"1+{number}1"))