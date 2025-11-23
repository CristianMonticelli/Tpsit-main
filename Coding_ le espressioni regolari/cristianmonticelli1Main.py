import cristianmonticelli1

if __name__ == "__main__":
    # input separato nel main: evita esecuzione all'import del modulo
    espressioneinput = input("espressione regolare: ")
    esp = cristianmonticelli1.EsprReg()
    esp.set_pattern(espressioneinput)  # uso del metodo che riceve l'espressione
    stringaInput = input("stringa da controllare: ")
    controllo = esp.matching(stringaInput)
    print(controllo)


