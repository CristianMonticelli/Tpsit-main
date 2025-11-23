import cristianmonticelli1
if __name__ == "__main__":
    espressioneinput = input("espressione regolare:")
    espresione1 = cristianmonticelli1.EsprReg(espressioneinput)
    stringaInput = input("stringa da controllare:")
    controllo = espresione1.matching(stringaInput)
    print(controllo)


