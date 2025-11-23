import re
import random

studenti = [
    "Luca Ciaone", "Matteo Parmiciaoli", "Claudio Rossi", "Luigi Macioni",
    "Gino Ricci", "Gino Belli", "Anna Verdi", "Maria Neri",
    "Paolo Bianchi", "Sara Gialli"
]


def scegli_estratti(candidati):
    if len(candidati) <= 3:
        return candidati.copy()
    return random.sample(candidati, 3)


def match_atomo(stringa, lista):
    pattern = re.escape(stringa)
    print(f"Provo ATOMO: {pattern}")
    filtrati = []

    for nome in lista:
        if re.search(pattern, nome):
            filtrati.append(nome)

    return filtrati


def match_gruppo(stringa, lista):
    chars = "".join(re.escape(c) for c in stringa)
    pattern = f"[{chars}]"

    print(f"Provo GRUPPO: {pattern}")
    filtrati = []

    for nome in lista:
        if re.search(pattern, nome):
            filtrati.append(nome)

    return filtrati



def match_range(stringa, lista):
    s_lower = stringa.lower()
    minimo = min(s_lower)
    massimo = max(s_lower)

    pattern = f"[{minimo}-{massimo}{minimo.upper()}-{massimo.upper()} ]"

    print(f"Provo RANGE: {pattern}")
    filtrati = []

    for nome in lista:
        if re.search(pattern, nome):
            filtrati.append(nome)

    return filtrati



def filtra_con_priorita(stringa):

    # PRIORITÀ 1 → atomo
    f1 = match_atomo(stringa, studenti)
    if f1:
        print("→ Usato ATOMO")
        return f1

    # PRIORITÀ 2 → gruppo
    f2 = match_gruppo(stringa, studenti)
    if f2:
        print("→ Usato GRUPPO")
        return f2

    # PRIORITÀ 3 → range
    f3 = match_range(stringa, studenti)
    if f3:
        print("→ Usato RANGE")
        return f3

    return []


