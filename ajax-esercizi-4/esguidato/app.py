from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cerca", methods=["GET"])
def cerca():
    query = request.args.get("q")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM localita WHERE nome LIKE ?", ('%' + query + '%',))
    risultati = cur.fetchall()

    data = []
    for r in risultati:
        data.append({
            "nome": r["nome"],
            "provincia": r["provincia"]
        })

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)