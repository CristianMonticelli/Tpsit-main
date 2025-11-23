from cristianmonticelli2 import filtra_con_priorita, scegli_estratti

def main():

    stringaInput = input("Inserisci stringa da filtrare: ")

    matchati = filtra_con_priorita(stringaInput)

    print("\nNominativi filtrati:", matchati)

    estratti = scegli_estratti(matchati)

    print("Nominativi estratti:", estratti)


if __name__ == "__main__":
    main()
