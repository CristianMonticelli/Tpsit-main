# Guida Completa: Come Fare i 4 Esercizi AJAX del Screenshot

## Introduzione
Questi esercizi usano **AJAX (Asynchronous JavaScript and XML)** con `XMLHttpRequest` per caricare contenuti HTML dinamicamente senza ricaricare la pagina. Funziona solo con **server locale** (non `file://` per CORS).

**Comando test**: `cd ajax-esercizi-4 && python3 -m http.server 8000` → `http://localhost:8000/esercizio1.html`

## Concetti Base Comuni a Tutti gli Esercizi
```javascript
const xhr = new XMLHttpRequest();  // Crea oggetto AJAX
xhr.onload = () => {               // Callback su completamento
    if (xhr.status === 200) {
        elemento.innerHTML = xhr.responseText;  // Inserisci HTML
    }
};
xhr.open('GET', 'file.html', true);  // GET asincrono (true=async)
xhr.send();                          // Invia richiesta
```

**Eventi**:
- `onmouseenter` per hover mouse.
- `onchange` per menu `<select>`.

---

## Esercizio 1: Hover su 2 Stringhe → 2 Zone Distinte
**Obiettivo**: Mouse su testo → carica 2 docs diversi in 2 `<div>`.

**Codice chiave in `esercizio1.html`**:
```html
<span onmouseenter="caricaDoc1()">Carica Doc1</span>
<div id="zona1">Zona 1</div>
```
```javascript
function caricaDoc1() {
    const xhr = new XMLHttpRequest();
    xhr.onload = () => document.getElementById('zona1').innerHTML = xhr.responseText;
    xhr.open('GET', 'doc1.html', true);
    xhr.send();
}
```
**Spiegazione**: `onmouseenter` lancia funzione che fa AJAX GET su `doc1.html` e sostituisce contenuto `#zona1`.

**File**: `doc1.html`, `doc2.html` = semplici HTML snippets.

---

## Esercizio 2: Menu 3 Opzioni → 3 Div Specifici
**Obiettivo**: `<select>` sceglie doc → carica in div corrispondente.

**Struttura HTML**:
```html
<div id="zona1">zona di visualizzazione source1.htm</div>
<select onchange="caricaSelezionato()">
    <option value="source1.html">source1.htm</option>
</select>
```
**JS**:
```javascript
function caricaSelezionato() {
    const val = document.getElementById('menu').value;
    const num = val.match(/source(\\d)/)[1];  // Estrae '1' da 'source1.html'
    // ... AJAX ...
    document.getElementById('zona' + num).innerHTML = ...;
}
```
**Spiegazione**: `onchange` estrae numero dal filename, targetta `zonaN`.

---

## Esercizio 3: 2 Liste 4 Stringhe → 8 Docs in 2 Zone
**Obiettivo**: 8 hover → 4 docs/lista in zona dedicata.

**HTML**:
```html
<div class="item" onmouseenter="carica('a1.html', 'sinistra')">Stringa A1</div>
<div id="zona-sinistra">Zona sinistra</div>
```
**JS**:
```javascript
function carica(url, zona) {
    // AJAX ...
    document.getElementById('zona-' + zona).innerHTML = ...;
}
```
**Spiegazione**: Parametro `zona` seleziona target sinistro/destro.

---

## Esercizio 4: Menu 6 Opzioni → 6 Docs in 3 Span (2 per Span)
**Obiettivo**: `<select>` 6 docs → gruppi di 2 in ogni `<span>`.

**JS Logica**:
```javascript
const num = parseInt(val.match(/index(\\d)/)[1]);  // 1-6
const z = Math.floor((num-1)/2) + 1;  // 1→1, 2→1, 3→2, 4→2, 5→3, 6→3
document.getElementById('zona' + z).innerHTML = ...;
```
**Spiegazione**: `Math.floor((num-1)/2)+1` mappa: 1-2→zona1, 3-4→zona2, 5-6→zona3.

---

## Risoluzione Problemi Comuni
| Problema | Soluzione |
|----------|-----------|
| "CORS error" | Usa server (`python3 -m http.server`) |
| "Empty zone" | Controlla filename esatti, status 200 |
| Hover multipli | OK, ricarica ogni hover |
| Select non funziona | `onchange`, value corretto |

## Test Completo
1. Apri ogni `esercizioN.html`.
2. Esegui azioni (hover/select).
3. Verifica caricamento in zone corrette.

Codice minimale, puro vanilla JS + XMLHttpRequest. Pronto per TPSIT!

**Tempo sviluppo**: ~30min/esercizio.

