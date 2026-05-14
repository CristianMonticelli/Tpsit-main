from flask import Blueprint, render_template, request, jsonify
from . import db

# Blueprint named 'bp' so it can be registered by the application factory
bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/cerca', methods=['GET'])
def cerca():
    query = request.args.get('q', '')
    # Log query for debugging (appears on server stdout)
    print(f"/cerca query: '{query}'")

    conn = db.get_db()
    cur = conn.cursor()

    # Cerca il nome nella tabella `comuni` e unisce con la tabella `provincie`
    sql = (
        "SELECT c.name AS nome, p.name AS provincia "
        "FROM comuni c LEFT JOIN provincie p ON c.codice_provincia_istat = p.codice_provincia_istat "
        "WHERE c.name LIKE ? LIMIT 100"
    )
    cur.execute(sql, ('%' + query + '%',))
    risultati = cur.fetchall()

    data = []
    for r in risultati:
        # sqlite3.Row supports both indexing and mapping by column name
        try:
            nome = r['nome']
            provincia = r['provincia']
        except Exception:
            nome = r[0]
            provincia = r[1] if len(r) > 1 else ''

        data.append({
            'nome': nome,
            'provincia': provincia or ''
        })

    return jsonify(data)