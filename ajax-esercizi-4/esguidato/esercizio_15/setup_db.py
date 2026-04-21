import sqlite3
import os
import re

# Definiamo dove creare il file del database (nella cartella instance)
if not os.path.exists('instance'):
    os.makedirs('instance')

db_path = os.path.join('instance', 'localita.sqlite')

# If a previous DB exists, remove it so setup is idempotent and starts clean
if os.path.exists(db_path):
    try:
        os.remove(db_path)
    except OSError:
        pass

# Ci connettiamo (se il file non esiste, lo crea)
connection = sqlite3.connect(db_path)


def sanitize_mysql_dump(sql_text: str) -> str:
    """Remove MySQL-specific statements so the dump can be executed by sqlite3.

    This keeps CREATE TABLE / INSERT statements but strips:
      - CREATE DATABASE / USE
      - MySQL versioned comments like /*!40101 ... */
      - ENGINE=..., DEFAULT CHARSET=..., AUTO_INCREMENT=... table options
      - ALTER TABLE ... DISABLE/ENABLE KEYS
      - backticks, unsigned, and size qualifiers like int(10)
    """
    # remove MySQL versioned comments (e.g. /*!40101 SET ... */;)
    sql_text = re.sub(r'/\*!\d+[\s\S]*?\*/;?', '', sql_text)

    # convert MySQL-style backslash-escaped single quotes to SQL-standard doubled single quotes
    sql_text = sql_text.replace("\\'", "''")

    # remove CREATE DATABASE and USE statements
    sql_text = re.sub(r'CREATE\s+DATABASE[\s\S]*?;\s*', '', sql_text, flags=re.IGNORECASE)
    sql_text = re.sub(r'USE\s+[^;]+;\s*', '', sql_text, flags=re.IGNORECASE)

    # Convert UNIQUE KEY (...) to SQLite-compatible UNIQUE (...)
    sql_text = re.sub(r'UNIQUE\s+KEY\s+[^\(]*\(([^)]+)\)', r'UNIQUE (\1)', sql_text, flags=re.IGNORECASE)
    # Remove non-unique KEY <name> (cols) by replacing 'KEY name (' with '('
    sql_text = re.sub(r'\bKEY\s+\w+\s*\(', '(', sql_text, flags=re.IGNORECASE)

    # remove ALTER TABLE ... DISABLE/ENABLE KEYS lines
    sql_text = re.sub(r"ALTER TABLE [^;]*DISABLE KEYS\s*;\s*", '', sql_text, flags=re.IGNORECASE)
    sql_text = re.sub(r"ALTER TABLE [^;]*ENABLE KEYS\s*;\s*", '', sql_text, flags=re.IGNORECASE)

    # remove table options: ) ENGINE=InnoDB AUTO_INCREMENT=123 DEFAULT CHARSET=utf8;
    sql_text = re.sub(r'\)\s*ENGINE=[^;]*;', ');', sql_text, flags=re.IGNORECASE | re.DOTALL)
    sql_text = re.sub(r'DEFAULT CHARSET=[^;\s]+', '', sql_text, flags=re.IGNORECASE)
    sql_text = re.sub(r'AUTO_INCREMENT=\d+', '', sql_text, flags=re.IGNORECASE)

    # remove inline AUTO_INCREMENT tokens left in column definitions
    sql_text = re.sub(r'\bAUTO_INCREMENT\b', '', sql_text, flags=re.IGNORECASE)

    # remove unsigned keyword
    sql_text = re.sub(r'\bunsigned\b', '', sql_text, flags=re.IGNORECASE)

    # simplify type sizes: int(10) -> int, bigint(20) -> bigint
    sql_text = re.sub(r'(\b[a-z]+)\(\d+\)', r"\1", sql_text, flags=re.IGNORECASE)

    # remove backticks
    sql_text = sql_text.replace('`', '')

    # Optionally remove any MySQL-specific ENGINE/ROW_FORMAT hints left
    sql_text = re.sub(r'ROW_FORMAT=[^;\s]+', '', sql_text, flags=re.IGNORECASE)

    # remove stray commas before closing parens caused by removed tokens
    sql_text = re.sub(r',\s*\)', ')', sql_text)
    # remove stray commas before semicolons
    sql_text = re.sub(r',\s*;', ';', sql_text)
    # collapse multiple spaces/tabs to single space for cleanliness
    sql_text = re.sub(r'[ \t]+', ' ', sql_text)

    return sql_text


try:
    # Leggiamo lo schema SQL e lo ripuliamo
    with open('app/localita.sql', encoding='utf-8') as f:
        raw_sql = f.read()

    clean_sql = sanitize_mysql_dump(raw_sql)

    # Eseguiamo lo script ripulito statement-per-statement to get better diagnostics
    statements = [s.strip() for s in clean_sql.split(';') if s.strip()]
    for idx, stmt in enumerate(statements, start=1):
        try:
            # sqlite3.executescript accepts a full script; we add trailing semicolon
            connection.executescript(stmt + ';')
        except sqlite3.Error as e:
            print(f"Errore sqlite3 sulla statement {idx}:", e)
            # show a compact snippet to help debugging
            snippet = stmt.replace('\n', ' ')[:300]
            print('Statement snippet:', snippet)
            raise
    print("Database creato con successo in:", db_path)
except sqlite3.Error as e:
    print("Errore sqlite3 durante la creazione del DB:", e)
finally:
    connection.close()