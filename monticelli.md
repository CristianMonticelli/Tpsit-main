
# Esercizio markdown

## Obiettivo dell'esercizio
+ Usare **vari livelli** per titolo, sottotitolo e testo[^1]
+ Scrivere le informazioni più importanti in **grassetto** e/o *corsivo*
+ >Realizzare delle *note a piè di pagina*[^2]
+ Realizzare una checklist per le risposte[^3]

---

# Esercizio su YAML, XML e XSD

## Realizzare in YAML una rubrica dove si legga:

1. il **nome** dell'alunno/a, 
2. il **voto** *pratico*, 
3. quello *teorico*, 
4. se insufficiente **calcolando la media** e scrivendo sì/no
5. un **commento** sulla prova sostenuta.

### File creati:

#### YAML (yamlmonticelli.yml)
Rubrica con i dati dello studente **Lorenzo Sanchez**:
- Voto pratico: 7
- Voto teorico: 5  
- Media: 6
- Insufficiente: no
- Commento: *Bravo ma non si applica*

#### XML (rubrica.xml)
Conversione della rubrica YAML in formato XML con struttura ben formattata.

#### XSD (rubrica.xsd)
Schema di validazione che definisce:
- **Tipi di dati**: string, int, decimal
- **Restrizioni**: voti da 1 a 10, media con una cifra decimale
- **Enumerazioni**: campo insufficiente (sì/no)

> Per validare lo schema YAML puoi usare questo editor online: https://codebeautify.org/yaml-editor-online[^4]



## Domande di Verifica (Checklist)

### Domanda 1: Il file YAML contiene tutti gli elementi richiesti?
- [ ] Nome dell'alunno presente
- [ ] Voto pratico definito
- [ ] Voto teorico definito  
- [ ] Media calcolata
- [ ] Indicazione insufficiente (sì/no)
- [ ] Commento sulla prova

### Domanda 2: La conversione XML è corretta?
- [ ] Struttura XML ben formattata
- [ ] Elementi corrispondenti al YAML
- [ ] Dati dello studente preservati
- [ ] Sintassi XML valida

### Domanda 3: Lo schema XSD è completo?
- [ ] Definizione dei tipi di dati
- [ ] Restrizioni sui valori dei voti
- [ ] Enumerazioni per campo insufficiente
- [ ] Validazione della struttura XML

---

## Riferimenti

[^1]: Utilizzo di heading multipli (# ## ###) per gerarchia del contenuto
[^2]: Note esplicative aggiunte al documento per chiarimenti aggiuntivi
[^3]: Lista di controllo con checkbox per tracking dei task completati  
[^4]: Risorsa online per validazione e editing di file YAML
