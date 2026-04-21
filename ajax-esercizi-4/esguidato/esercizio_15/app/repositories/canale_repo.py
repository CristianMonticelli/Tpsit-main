from app.db import get_db

def get_canale():
    db = get_db()
    query = '''
            SELECT id, nome, numero_iscritti, categoria_id
            FROM canali 
            ORDER BY numero_iscritti DESC'''
       
        
    channels = db.execute(query).fetchall()
    return [dict(channel) for channel in channels]

def get_canale_id(id):
    db = get_db()
    query = '''
            SELECT id, nome, numero_iscritti, categoria_id
            FROM canali 
            WHERE id=?'''
    print("--------------------------------------------------------")
    print(query)
        
    channel = db.execute(query,(id,)).fetchone()
    if channel:
        return dict(channel)
    return None


def create_channel(nome: str, numero_iscritti: int, categoria: str) -> None:
    db = get_db()
    query = '''
            INSERT INTO canali (nome, numero_iscritti, categoria)
            VALUES (?, ?, ?)'''
    cursor = db.execute(query, (nome, numero_iscritti, categoria))
    db.commit()
    return cursor.lastrowid
