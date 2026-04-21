from app.db import get_db




def get_video_id(id):
    db = get_db()
    query = '''
            SELECT id, canale_id, titolo
            FROM video 
            WHERE canale_id=?'''
    
        
    channels = db.execute(query,(id,)).fetchall()
    return [dict(channel) for channel in channels]


def create_video(canale_id: str, titolo: str, durata: int, immagine: str) -> None:
    db = get_db()
    query = '''
            INSERT INTO video (canale_id, titolo, durata, immagine)
            VALUES (?, ? ,?,?)'''
    cursor = db.execute(query, (canale_id, titolo, durata, immagine))
    db.commit()
    return cursor.lastrowid

