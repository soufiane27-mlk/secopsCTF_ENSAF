import string

code = input("gol chno bghiti yalah > ")

rak_dayz = all([(char in string.printable) for char in code])

if rak_dayz:
    sayn_sayn_nchof = all([(char in string.ascii_lowercase + " ") for char in code])
    if sayn_sayn_nchof :
        exec(code)
        exit(sayn_sayn_nchof)
    elif all([(char in string.punctuation+string.digits) for char in code]):
        print("wach bghiti t7ssab chi 7aja ??")
        value = eval(code, {"__builtins__": None})
        print(f"{code} = {value}")
    else:
        print("ylah ghyrha !!!!")
        exit()
exit()