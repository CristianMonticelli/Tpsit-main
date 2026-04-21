from app.db import get_db



def get_categoria():
    db = get_db()
    query = '''
            SELECT id, nome  
            FROM categoria 
            '''
       
        
    categorie = db.execute(query).fetchall()
    return [dict(categoria) for categoria in categorie]


def create_category(nome) -> None:
    db = get_db()
    query = '''
            INSERT INTO categoria (nome)
            VALUES (?)'''
    cursor = db.execute(query, (nome,))
    db.commit()
    return cursor.lastrowid
