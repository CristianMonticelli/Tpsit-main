# Esercizio markdown
+ Usare vari livelli per titolo, sottotitolo e testo
+ Scrivere le informazioni più importanti in grassetto e/o corsivo
+ Realizzare delle note a piè di pagina 
+ Realizzare 3 domande usando una checklist per le risposte.

# Espressioni regolari in python
#### Creare nel linguaggio di programmazione che preferisci (PHP, C#, Java, ...) una classe (ad es. EsprReg) che data una espressione regolare e una stringa valida quest'ultima, ovvero restituisce a video il testo "match" oppure "mismatch".
## In particolare si vogliono vedere:

1. *attributi e metodi* con gli opportuni **modificatori** di classe
2. ***almeno due metodi*** di cui **uno** che riceve in input l'espressione regolare e l'altro che effettua il test per la validazione e restituisce l'output suddetto
3. il *costruttore della vostra classe* (potete anche estenderne una già prevista se preferite) e *un'istanza della vostra classe* nel main in cui vengono richiamati i metodi di cui sopra 
4. in alternativa potete anche *creare una classe di utilità con metodi* e proprietà statici e utilizzarla **opportunamente nel main** in cui vengono richiamati i metodi di cui sopra
5. ***codice ben indentato, commentato e modulare*** (ovvero un file dedicato per ogni parte logica del programma). 

## N.B.:
>+ il tutto va versionato in un repository nel vostro GitHub.
>+ La consegna prevede il link al vostro repository!
>+ Non c'è tanto codice da scrivere, fatemi vedere che avete capito entrambi i concetti: versionamento (i vari comandi di git) e espressioni regolari.
>+ Per domande tecniche sul linguaggio di programmazione scelto chiedete al vostro docente di Informatica che sicuramente è più bravo di me :)

## Esercizio python
```
class EsprReg:
    def __init__(self, espressioneRegolare):
        self._espressioneRegolare = espressioneRegolare
    @property
    def espressioneRegolare(self):
        return self._espressioneRegolare
    @espressioneRegolare.setter
    def espressioneRegolare(self,new_espressioneRegolare):
        self._espressioneRegolare = new_espressioneRegolare
    def matching(self, stringa):
        pattern = re.compile(self._espressioneRegolare)
        matching = pattern.match (stringa)
        if matching == None:
            return "mismatch"
        else:
            return "match"
espressioneinput = input("espressione regolare:")
espresione1 = EsprReg(espressioneinput)
stringaInput = input("stringa da controllare:")
controllo = espresione1.matching(stringaInput)
print(controllo)
```
## Check list
- [x] attributi
- [x] almeno due metodi
- [x] costruttore della vostra classe
- [ ] codice ben indentato, commentato e modulare