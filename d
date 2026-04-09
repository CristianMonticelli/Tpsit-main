# Spiegazione e come rifare — inserimento.html e visualizza.html

Breve panoramica
- Scopo: gestire un registro di studenti lato client usando LocalStorage + sessionStorage.
  - inserimento.html: form, validazione client-side, salva il record e memorizza l'ultimo inserito in sessionStorage.
  - visualizza.html: legge il registro da LocalStorage, mostra tabella, permette eliminare singoli record, cancellare tutto ed esportare JSON.

Schema dati consigliato
- LocalStorage key: `registro`
- Struttura consigliata:
  {
    "students": [
      {
        "id": 1679999999999,
        "nome": "Mario",
        "cognome": "Rossi",
        "data_nascita": "2000-01-01",
        "codice_fiscale": "RSSMRA00A01H501A",
        "classe": "3",
        "sezione": "A",
        "ripetente": false,
        "anni_ripetuti": 0,
        "uscita": "università"
      }
    ]
  }
- Usare `id` univoco (es. Date.now() o UUID) invece di fare dipendenza dall'indice array.

Come funziona oggi (punti principali)
- inserimento.html
  - Validazioni su nome/cognome (regex), data di nascita (deve essere nel passato e >=18 anni), CF (formato semplificato), ripetente -> anni obbligatori >0.
  - Al submit: crea oggetto studente, lo aggiunge a `registro.books` in LocalStorage, salva `ultimoStudente` in sessionStorage e reindirizza a `risultato.html`.
  - Toggle visibilità campo anni_ripetuti in base alla checkbox ripetente.
  - Problemi osservati: select con `multiple` (probabilmente non voluto), uso di `books` nome confuso, eliminazione in visualizza basata su indice (fragile), innerHTML per rendering (rischio injection).
- visualizza.html
  - Carica `registro` da LocalStorage e costruisce una tabella via stringhe HTML.
  - Mostra totale studenti, elimina con splice(index) e salva cambio.
  - Esporta JSON creando un Blob e forzando il download.

Problemi e miglioramenti consigliati
- Rinominare `books` → `students` per chiarezza.
- Rimuovere `multiple` dalle select se deve essere scelta singola.
- Usare id univoci per cancellazioni: elimina per id, non per indice.
- Separare JS e CSS in file esterni (assets/js/app.js, assets/css/styles.css).
- Creare funzioni di storage riutilizzabili: loadRegistro(), saveRegistro(), addStudent(), deleteStudentById().
- Usare DOM API (createElement / textContent) invece di innerHTML per evitare injection e migliorare accessibilità.
- Aggiungere conferme prima delle cancellazioni e messaggi utente accessibili (aria-live).
- Migliorare validazione del CF solo se serve; altrimenti indicare che è valida solo la forma base.
- Gestire casi di importazione/export e backup.

Passi suggeriti per rifare i file (rapido how‑to)
1. Creare structure:
   - inserimento.html (solo markup e include di assets/js/form.js e assets/css/styles.css)
   - visualizza.html (markup, include assets/js/view.js)
   - assets/js/storage.js (load/save/add/delete)
   - assets/js/validation.js (validatori)
   - assets/css/styles.css

2. Implementare API di storage (esempio minimo):
```javascript
// esempio: assets/js/storage.js
function loadRegistro() {
  return JSON.parse(localStorage.getItem('registro') || '{"students":[]}');
}
function saveRegistro(registro) {
  localStorage.setItem('registro', JSON.stringify(registro, null, 2));
}
function addStudent(student) {
  const r = loadRegistro();
  student.id = Date.now();
  r.students.push(student);
  saveRegistro(r);
}
function deleteStudentById(id) {
  const r = loadRegistro();
  r.students = r.students.filter(s => s.id !== id);
  saveRegistro(r);
}
```

3. Inserimento (form.js)
- Validare campi.
- Costruire oggetto studente.
- Chiamare addStudent(student).
- Salvare sessionStorage.setItem('ultimoStudente', JSON.stringify(student)).
- Reset form e redirect a risultato.html.

4. Visualizza (view.js)
- Leggere registro con loadRegistro().
- Render tabella con createElement / textContent; ogni riga avere data-id.
- Elimina: leggere data-id e chiamare deleteStudentById(id), poi rerender.
- Esporta: JSON Blob come oggi.
- Aggiornare contatore totale.

5. UI / accessibilità
- Etichette associate (for / id).
- Errori mostrati in elemento con role="alert" / aria-live.
- Focus management: focus sul primo campo non valido.

Esempio di rendering sicuro (snippet)
```javascript
// renderTable(container)
const r = loadRegistro();
const table = document.createElement('table');
const tbody = document.createElement('tbody');
r.students.forEach((s, i) => {
  const tr = document.createElement('tr');
  const tdIndex = document.createElement('td'); tdIndex.textContent = i+1; tr.appendChild(tdIndex);
  const tdNome = document.createElement('td'); tdNome.textContent = s.nome; tr.appendChild(tdNome);
  // ... altri campi
  const tdActions = document.createElement('td');
  const btn = document.createElement('button'); btn.textContent = 'Elimina';
  btn.dataset.id = s.id;
  btn.addEventListener('click', () => { if(confirm('Confermi?')) { deleteStudentById(s.id); renderTable(); }});
  tdActions.appendChild(btn); tr.appendChild(tdActions);
  tbody.appendChild(tr);
});
table.appendChild(tbody);
container.innerHTML = ''; container.appendChild(table);
```

File aggiuntivi consigliati
- risultato.html: mostra JSON di sessionStorage 'ultimoStudente' con possibilità di tornare a inserimento o visualizza.
- README.md: istruzioni su struttura e come eseguire (apri file in browser).

Vuoi che generi i file rifatti (inserimento.html, visualizza.html, assets/js/storage.js, assets/js/form.js, assets/js/view.js, assets/css/styles.css) già pronti nel percorso del progetto? Posso crearli ora.// filepath: /home/monticelli/utile/Tpsit-main/compiti_Validazione_form/spiegazione.md

# Spiegazione e come rifare — inserimento.html e visualizza.html

Breve panoramica
- Scopo: gestire un registro di studenti lato client usando LocalStorage + sessionStorage.
  - inserimento.html: form, validazione client-side, salva il record e memorizza l'ultimo inserito in sessionStorage.
  - visualizza.html: legge il registro da LocalStorage, mostra tabella, permette eliminare singoli record, cancellare tutto ed esportare JSON.

Schema dati consigliato
- LocalStorage key: `registro`
- Struttura consigliata:
  {
    "students": [
      {
        "id": 1679999999999,
        "nome": "Mario",
        "cognome": "Rossi",
        "data_nascita": "2000-01-01",
        "codice_fiscale": "RSSMRA00A01H501A",
        "classe": "3",
        "sezione": "A",
        "ripetente": false,
        "anni_ripetuti": 0,
        "uscita": "università"
      }
    ]
  }
- Usare `id` univoco (es. Date.now() o UUID) invece di fare dipendenza dall'indice array.

Come funziona oggi (punti principali)
- inserimento.html
  - Validazioni su nome/cognome (regex), data di nascita (deve essere nel passato e >=18 anni), CF (formato semplificato), ripetente -> anni obbligatori >0.
  - Al submit: crea oggetto studente, lo aggiunge a `registro.books` in LocalStorage, salva `ultimoStudente` in sessionStorage e reindirizza a `risultato.html`.
  - Toggle visibilità campo anni_ripetuti in base alla checkbox ripetente.
  - Problemi osservati: select con `multiple` (probabilmente non voluto), uso di `books` nome confuso, eliminazione in visualizza basata su indice (fragile), innerHTML per rendering (rischio injection).
- visualizza.html
  - Carica `registro` da LocalStorage e costruisce una tabella via stringhe HTML.
  - Mostra totale studenti, elimina con splice(index) e salva cambio.
  - Esporta JSON creando un Blob e forzando il download.

Problemi e miglioramenti consigliati
- Rinominare `books` → `students` per chiarezza.
- Rimuovere `multiple` dalle select se deve essere scelta singola.
- Usare id univoci per cancellazioni: elimina per id, non per indice.
- Separare JS e CSS in file esterni (assets/js/app.js, assets/css/styles.css).
- Creare funzioni di storage riutilizzabili: loadRegistro(), saveRegistro(), addStudent(), deleteStudentById().
- Usare DOM API (createElement / textContent) invece di innerHTML per evitare injection e migliorare accessibilità.
- Aggiungere conferme prima delle cancellazioni e messaggi utente accessibili (aria-live).
- Migliorare validazione del CF solo se serve; altrimenti indicare che è valida solo la forma base.
- Gestire casi di importazione/export e backup.

Passi suggeriti per rifare i file (rapido how‑to)
1. Creare structure:
   - inserimento.html (solo markup e include di assets/js/form.js e assets/css/styles.css)
   - visualizza.html (markup, include assets/js/view.js)
   - assets/js/storage.js (load/save/add/delete)
   - assets/js/validation.js (validatori)
   - assets/css/styles.css

2. Implementare API di storage (esempio minimo):
```javascript
// esempio: assets/js/storage.js
function loadRegistro() {
  return JSON.parse(localStorage.getItem('registro') || '{"students":[]}');
}
function saveRegistro(registro) {
  localStorage.setItem('registro', JSON.stringify(registro, null, 2));
}
function addStudent(student) {
  const r = loadRegistro();
  student.id = Date.now();
  r.students.push(student);
  saveRegistro(r);
}
function deleteStudentById(id) {
  const r = loadRegistro();
  r.students = r.students.filter(s => s.id !== id);
  saveRegistro(r);
}
```

3. Inserimento (form.js)
- Validare campi.
- Costruire oggetto studente.
- Chiamare addStudent(student).
- Salvare sessionStorage.setItem('ultimoStudente', JSON.stringify(student)).
- Reset form e redirect a risultato.html.

4. Visualizza (view.js)
- Leggere registro con loadRegistro().
- Render tabella con createElement / textContent; ogni riga avere data-id.
- Elimina: leggere data-id e chiamare deleteStudentById(id), poi rerender.
- Esporta: JSON Blob come oggi.
- Aggiornare contatore totale.

5. UI / accessibilità
- Etichette associate (for / id).
- Errori mostrati in elemento con role="alert" / aria-live.
- Focus management: focus sul primo campo non valido.

Esempio di rendering sicuro (snippet)
```javascript
// renderTable(container)
const r = loadRegistro();
const table = document.createElement('table');
const tbody = document.createElement('tbody');
r.students.forEach((s, i) => {
  const tr = document.createElement('tr');
  const tdIndex = document.createElement('td'); tdIndex.textContent = i+1; tr.appendChild(tdIndex);
  const tdNome = document.createElement('td'); tdNome.textContent = s.nome; tr.appendChild(tdNome);
  // ... altri campi
  const tdActions = document.createElement('td');
  const btn = document.createElement('button'); btn.textContent = 'Elimina';
  btn.dataset.id = s.id;
  btn.addEventListener('click', () => { if(confirm('Confermi?')) { deleteStudentById(s.id); renderTable(); }});
  tdActions.appendChild(btn); tr.appendChild(tdActions);
  tbody.appendChild(tr);
});
table.appendChild(tbody);
container.innerHTML = ''; container.appendChild(table);
```

File aggiuntivi consigliati
- risultato.html: mostra JSON di sessionStorage 'ultimoStudente' con possibilità di tornare a inserimento o visualizza.
- README.md: istruzioni su struttura e come eseguire (apri file in browser).

Vuoi che generi i file rifatti (inserimento.html, visualizza.html, assets/js/storage.js, assets/js/form.js, assets/js/view.js, assets/css/styles.css) già pronti nel percorso del progetto? Posso crearli ora.
