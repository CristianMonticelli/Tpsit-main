"""
ESERCIZIO LABORATORIO 2 - VERSIONE COMPLETA
Applicazione Flask che replica l'esempio del libro (PHP+MySQL) usando Python+SQLite.
Funzionalità: ricerca comuni italiani con meccanismo tipo "Google Suggest" via AJAX.

AVVIO:
  1. pip install flask
  2. python app_completo.py
  3. Apri il browser su http://localhost:5000
"""

import sqlite3
import os
import re
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
DB_PATH = "localita.db"
SQL_PATH = "localita.sql"  # metti il file SQL nella stessa cartella

# ─────────────────────────────────────────────
# SETUP DATABASE: crea SQLite dal dump MySQL
# ─────────────────────────────────────────────
def init_db():
    """Legge localita.sql e popola il database SQLite (solo al primo avvio)."""
    if os.path.exists(DB_PATH):
        return  # già creato

    print("Primo avvio: creo il database SQLite da localita.sql ...")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Crea la tabella comuni
    cur.execute("""
        CREATE TABLE IF NOT EXISTS comuni (
            ID      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT NOT NULL,
            slug    TEXT,
            lat     TEXT,
            lng     TEXT,
            codice_provincia_istat      TEXT,
            codice_comune_istat         TEXT,
            codice_alfanumerico_istat   TEXT,
            capoluogo_provincia         INTEGER,
            capoluogo_regione           INTEGER
        )
    """)

    # Legge il file SQL ed estrae i blocchi INSERT
    with open(SQL_PATH, "r", encoding="utf-8", errors="replace") as f:
        sql_text = f.read()

    # Trova tutti i valori nei blocchi INSERT INTO comuni ... VALUES (...)
    # Il file usa righe separate da virgola, ogni tupla è (...),
    pattern = re.compile(
        r"\((\d+),\s*'((?:[^'\\]|\\.|'')*)',\s*'((?:[^'\\]|\\.)*)',\s*'((?:[^'\\]|\\.)*)',\s*'((?:[^'\\]|\\.)*)',\s*'((?:[^'\\]|\\.)*)',\s*'((?:[^'\\]|\\.)*)',\s*'((?:[^'\\]|\\.)*)',\s*(\d+),\s*(\d+)\)"
    )

    rows = []
    for m in pattern.finditer(sql_text):
        # Ripristina gli apostrofi escaped (\' -> ')
        name = m.group(2).replace("\\'", "'").replace("''", "'")
        rows.append((
            int(m.group(1)),  # ID
            name,             # name
            m.group(3),       # slug
            m.group(4),       # lat
            m.group(5),       # lng
            m.group(6),       # codice_provincia_istat
            m.group(7),       # codice_comune_istat
            m.group(8),       # codice_alfanumerico_istat
            int(m.group(9)),  # capoluogo_provincia
            int(m.group(10)), # capoluogo_regione
        ))

    cur.executemany(
        "INSERT INTO comuni VALUES (?,?,?,?,?,?,?,?,?,?)", rows
    )
    conn.commit()
    conn.close()
    print(f"Database creato: {len(rows)} comuni inseriti.")


# ─────────────────────────────────────────────
# PAGINA HTML PRINCIPALE
# ─────────────────────────────────────────────
HTML = """
<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <title>Selezione comuni</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
    h2   { color: #333; }
    label { font-weight: bold; }
    #campo { padding: 6px 10px; font-size: 15px; width: 260px; border: 1px solid #aaa; border-radius: 4px; }
    #elenco {
      background: white;
      border: 1px solid #ccc;
      border-radius: 4px;
      width: 360px;
      max-height: 400px;
      overflow-y: auto;
      margin-top: 8px;
      padding: 8px;
      display: none;   /* nascosto finché non ci sono risultati */
    }
    .riga { padding: 4px 6px; cursor: pointer; border-bottom: 1px solid #eee; font-size: 14px; }
    .riga:hover { background: #e8f0fe; }
    .info { color: #666; font-size: 13px; margin-top: 6px; }
  </style>
</head>
<body>
  <h2>Selezione comuni italiani — tipo Google Suggest</h2>

  <label for="campo">Scrivi le iniziali del comune:</label><br><br>
  <input type="text" id="campo" placeholder="es. Mi, Roma, Lecco..."
         onkeyup="mostra(this.value)">

  <div id="elenco"></div>
  <p class="info" id="info"></p>

  <script>
    // ── AJAX: invia la stringa al server e riceve i risultati ──────────────────
    function mostra(str) {
      var elenco = document.getElementById("elenco");
      var info   = document.getElementById("info");

      // Se la casella è vuota, svuota e nascondi il div
      if (str.length === 0) {
        elenco.innerHTML = "";
        elenco.style.display = "none";
        info.textContent = "";
        return;
      }

      // Crea oggetto XMLHttpRequest (compatibile con tutti i browser moderni)
      var ajax;
      if (window.XMLHttpRequest) {
        ajax = new XMLHttpRequest();          // browser moderni
      } else {
        ajax = new ActiveXObject("Microsoft.XMLHTTP");  // IE6, IE5
      }

      // Callback: elabora la risposta del server
      ajax.onreadystatechange = function() {
        if (ajax.readyState === 4 && ajax.status === 200) {
          var dati = JSON.parse(ajax.responseText); // array di oggetti {name, lat, lng}

          info.textContent = "Trovati " + dati.length + " comuni.";

          if (dati.length === 0) {
            elenco.innerHTML = "<div class='riga'>Nessun comune trovato.</div>";
          } else {
            var html = "";
            for (var i = 0; i < dati.length; i++) {
              html += "<div class='riga'>"
                    + dati[i].name
                    + " &nbsp;<small style='color:#888'>(" + dati[i].lat + ", " + dati[i].lng + ")</small>"
                    + "</div>";
            }
            elenco.innerHTML = html;
          }
          elenco.style.display = "block";
        }
      };

      // Invia la richiesta GET al server Flask
      ajax.open("GET", "/cerca?stringa=" + encodeURIComponent(str), true);
      ajax.send();
    }
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)


# ─────────────────────────────────────────────
# ENDPOINT AJAX  →  /cerca?stringa=xxx
# Equivalente alla pagina elabora.php del libro
# ─────────────────────────────────────────────
@app.route("/cerca")
def cerca():
    stringa = request.args.get("stringa", "").strip()

    # Se la stringa è vuota restituisce lista vuota
    if len(stringa) == 0:
        return jsonify([])

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Query con LIKE: cerca i comuni il cui nome INIZIA con la stringa digitata
    # Il % finale = qualsiasi sequenza di caratteri dopo le iniziali
    query = "SELECT name, lat, lng FROM comuni WHERE name LIKE ? ORDER BY name"
    cur.execute(query, (stringa + "%",))

    risultati = [{"name": r["name"], "lat": r["lat"], "lng": r["lng"]}
                 for r in cur.fetchall()]
    conn.close()

    return jsonify(risultati)


# ─────────────────────────────────────────────
# AVVIO
# ─────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    print("Apri il browser su: http://localhost:5000")
    app.run(debug=True)
