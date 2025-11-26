import re

string = "Ciao, come va? Oggi è una bella giornata!"
pattern = r"[A-Z]"  
print(re.search(pattern, string))
# Output: <re.Match object; span=(0, 1), match='C'>
print(re.match(pattern, string))
# Output: <re.Match object; span=(0, 1), match='C'>
print(re.fullmatch(pattern, string))
# Output: None
print(re.findall(pattern, string))
# Output: ['C', 'O']


def cerca_maiuscole(string,pattern):
    risultato = re.search(pattern, string)
    return risultato


print(re.match(pattern, string))

print(re.fullmatch(pattern, string))

print(re.findall(pattern, string))