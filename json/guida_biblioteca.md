# Guida: Come funziona la mini-app Biblioteca (inserimento + visualizzazione)

Questa guida spiega come funzionano i file `inserimento.html` e `visualizza.html` (cartella `json`) presenti nel progetto. Troverai il modello dati, la spiegazione delle funzioni JavaScript principali, un "contratto" minimale (input/output), casi limite e un piano step‑by‑step per ricreare la stessa funzionalità da zero.

## Sommario rapido

- Dove guardare: `json/inserimento.html`, `json/visualizza.html`
- Dati persistenti: `localStorage` (chiave: `biblioteca`)
- Modello dati salvato: un oggetto con proprietà `books` (array di record libro)

---

## Modello dati

Nel `localStorage` viene salvato un JSON con questa struttura minima:

{
  "books": [
    {
      "titolo": "...",
      "autore": "...",
      "casaEditrice": "...",
      "annoEdizione": "...", // stringa o numero (se non specificato: "Non specificato")
      "genere": "...",
      "numeroPagine": "..." // stringa o numero (se non specificato: "Non specificato")
    },
    ...
  ]
}

Ogni elemento dell'array `books` è un oggetto che rappresenta un libro.

---

## Flusso generale dell'app

1. `inserimento.html` presenta un form HTML per inserire i dati di un libro.
2. Alla submit del form il JavaScript:
   - Previene il comportamento predefinito (ricarica pagina).
   - Costruisce un oggetto `nuovoLibro` con i valori presi dai campi.
   - Recupera la struttura esistente dal `localStorage` (funzione `caricaBiblioteca`).
   - Aggiunge `nuovoLibro` all'array `books`.
   - Salva di nuovo la struttura nel `localStorage` (funzione `salvaBiblioteca`).
   - Mostra un messaggio di conferma e resetta il form.
3. `visualizza.html` al caricamento chiama `visualizzaBiblioteca()` che:
   - Legge i dati dal `localStorage`.
   - Aggiorna il conteggio totale e genera HTML (una tabella) con i libri.
   - Fornisce azioni: eliminare un libro (index-based), svuotare tutta la biblioteca, esportare JSON.

---

## Funzioni JS principali (ed esatta logica)

Qui spiego le funzioni chiave e il perché.

### caricaBiblioteca()
- Scopo: recuperare dal `localStorage` la chiave `biblioteca` e ritornare un oggetto JS.
- Implementazione essenziale:

```javascript
function caricaBiblioteca() {
  const bibliotecaJSON = localStorage.getItem('biblioteca');
  if (bibliotecaJSON) return JSON.parse(bibliotecaJSON);
  return { books: [] };
}
```

- Error modes: JSON.parse può fallire se i dati sono corrotti. Nel codice fornito non c'è gestione dell'errore; in produzione conviene circondare con try/catch.

### salvaBiblioteca(biblioteca)
- Scopo: serializzare e salvare l'oggetto nel `localStorage`.

```javascript
function salvaBiblioteca(biblioteca) {
  const bibliotecaJSON = JSON.stringify(biblioteca, null, 2);
  localStorage.setItem('biblioteca', bibliotecaJSON);
}
```

- Nota: il `null, 2` serve a formattare l'JSON per renderlo leggibile se viene ispezionato.

### Gestione submit in `inserimento.html`
- Il form ha un event listener su `submit` che:
  - Preleva i valori con `document.getElementById(...).value`.
  - Costruisce l'oggetto `nuovoLibro` (con `.trim()` per i campi testuali).
  - Chiama `caricaBiblioteca()`, `biblioteca.books.push(nuovoLibro)` e `salvaBiblioteca(biblioteca)`.
  - Mostra un messaggio (funzione `mostraMessaggio`) e fa `this.reset()`.

### mostraMessaggio(testo, tipo)
- Aggiorna un div con testo e classi per lo stile (successo/errore) e lo rende visibile per qualche secondo.

### visualizzaBiblioteca() (in `visualizza.html`)
- Recupera i dati e se l'array è vuoto mostra un messaggio invitando ad aggiungere libri.
- Altrimenti costruisce una tabella HTML dinamicamente (string concatenation) e la inserisce in `innerHTML`.
- Ogni riga contiene un pulsante `Elimina` che chiama `eliminaLibro(index)`.

### eliminaLibro(index)
- Conferma con `confirm()` e poi fa `biblioteca.books.splice(index, 1)` seguita da `localStorage.setItem(...)` e `visualizzaBiblioteca()` per aggiornare la UI.

### cancellabiblioteca()
- `localStorage.removeItem('biblioteca')` e poi `visualizzaBiblioteca()`.

### esportaJSON()
- Costruisce un `Blob` da `JSON.stringify(biblioteca)` e usa un link temporaneo per forzare il download (`URL.createObjectURL`, `link.click()`).

---

## "Contratto" essenziale (inputs/outputs/assunzioni)

- Input: dati dal form (titolo, autore, casaEditrice, annoEdizione, genere, numeroPagine).
- Output: aggiornamento della chiave `biblioteca` in `localStorage` e aggiornamento interfaccia.
- Assunzioni: `localStorage` è disponibile e non pieno; i dati in `localStorage` sono JSON valido.
- Modalità di errore: attualmente non viene mostrato un messaggio esplicito se JSON.parse fallisce o se `localStorage` è pieno.

---

## Casi limite e problemi da considerare

1. Dati corrotti in `localStorage` (JSON.parse lancia eccezione).
2. Duplicati: l'app non controlla se lo stesso libro è già inserito.
3. Eliminazione basata su `index`: se si implementano filtri o ordinamenti cambierà l'index.
4. LocalStorage ha limiti di spazio (solitamente 5–10MB a seconda del browser).
5. Mancata validazione dei campi oltre all'attributo HTML `required` (es. anno fuori range, pagine negative).
6. Accessibilità: i pulsanti, i label e i feedback visivi possono essere migliorati.

---

## Come rifare (passo‑per‑passo)

1. Crea due file: `inserimento.html` e `visualizza.html`.
2. Nella pagina di inserimento aggiungi un `<form id="formLibro">` con campi text/number/select corrispondenti.
3. Aggiungi un listener JavaScript per `submit` che:
   - `e.preventDefault()`
   - Legge i valori dai campi (con `.trim()` per i testi)
   - Crei `nuovoLibro`
   - Recuperi la struttura con `caricaBiblioteca()` e poi `biblioteca.books.push(nuovoLibro)`
   - Salvi con `salvaBiblioteca(biblioteca)`
   - Mostri un messaggio e resetti il form
4. Nella pagina di visualizzazione, in `window.onload` chiama `visualizzaBiblioteca()` per:
   - Leggere i dati
   - Aggiornare il conteggio
   - Generare la tabella e collegare i pulsanti di azione
5. Implementa le funzioni `caricaBiblioteca`, `salvaBiblioteca`, `esportaJSON`, `eliminaLibro`, `cancellabiblioteca` come descritto sopra.

Esempio minimale per `caricaBiblioteca()` con gestione errori:

```javascript
function caricaBiblioteca() {
  const bibliotecaJSON = localStorage.getItem('biblioteca');
  if (!bibliotecaJSON) return { books: [] };
  try {
    return JSON.parse(bibliotecaJSON);
  } catch (err) {
    console.error('Errore parsing biblioteca da localStorage', err);
    // reset sicuro: sovrascrivi con struttura pulita
    const empty = { books: [] };
    localStorage.setItem('biblioteca', JSON.stringify(empty));
    return empty;
  }
}
```

---

## Miglioramenti suggeriti (proattivi)

- Aggiungere un `id` univoco per ogni libro (UUID) invece di usare l'index per eliminare.
- Implementare la modifica (edit) di un libro.
- Validazione più robusta lato JS (es. anno come numero in range, pagine > 0).
- Gestione degli errori di `localStorage` (spazio esaurito) con fallback (es. notifiche all'utente).
- Separare il codice JS in un file esterno `.js` e includerlo con `<script src="...">`.
- Usare template literals per creare DOM in modo più leggibile o usare DOM APIs (createElement/appendChild) per sicurezza XSS.
- Aggiungere filtri/ricerche e ordinamenti.

---

## Come testare durante lo sviluppo

- Apri `inserimento.html` in un browser (es. trascinando il file nella finestra del browser o con un server locale).
- Apri la Console DevTools (F12) per vedere eventuali errori.
- Inserisci un libro e poi vai su `visualizza.html` per verificare che appaia.
- Per resettare i dati manualmente: `localStorage.removeItem('biblioteca')` oppure usa la funzionalità "Cancella Tutto" nella UI.

Suggerimento rapido per sviluppo: usa l'estensione "Live Server" in VS Code o avvia un server semplice nella cartella con Python:

```bash
# dalla root del progetto
python3 -m http.server 8000
# poi apri http://localhost:8000/json/inserimento.html
```

---

## Piccolo checklist per ricrearlo da zero (sintetico)

- [ ] HTML form con id e attributi `required` per i campi obbligatori
- [ ] Funzioni JS: `caricaBiblioteca`, `salvaBiblioteca`, `mostraMessaggio`
- [ ] Submit handler: costruire `nuovoLibro`, push, save
- [ ] Pagina visualizza: `visualizzaBiblioteca()` con tabella e pulsanti
- [ ] Azioni: elimina libro, cancella tutto, esporta JSON
- [ ] Test manuale e gestione errori basica

---

## Dove ho messo questa guida

File creato: `json/guida_biblioteca.md`

---

## Conclusione

Nel repository sono presenti due pagine HTML autonome che comunicano solo via `localStorage`. Il codice è abbastanza semplice e ottimo come esercizio per comprendere il DOM, gli eventi, e la persistenza lato client. Se vuoi, posso:

- trasformare i blocchi JS in file separati `.js` e collegarli alle pagine;
- aggiungere ID univoci ai libri e implementare la modifica (edit);
- scrivere piccoli test automatici (es. script Puppeteer) che verificano l'inserimento e la visualizzazione.

Dimmi quale estensione preferisci e procedo con l'implementazione successiva.
