import sqlite3
from uuid import uuid4

conn = sqlite3.connect("db.db")
cur = conn.cursor()

def connect_to_db():
    cur.execute(
        "CREATE TABLE IF NOT EXISTS notes (id TEXT NOT NULL UNIQUE, text TEXT NOT NULL)"
    )


def get_notes():
    cur.execute("SELECT * FROM notes")
    data = cur.fetchall()
    return data


def create_note(text: str):
    id = str(uuid4())

    if text == "":
        return
    else:
        cur.execute(f"INSERT INTO notes VALUES ('{id}','{text}')")
        conn.commit()
        cur.execute(f"SELECT * FROM notes WHERE rowid = {cur.lastrowid}")
        new_note = cur.fetchone()
        return new_note


def delete_notes(note_ids: tuple):
    if len(note_ids) < 1:
        return
    elif len(note_ids) == 1:
        cur.execute(f"DELETE FROM notes WHERE id = '{note_ids[0]}'")
        conn.commit()
    else:
        cur.execute(f"DELETE FROM notes WHERE id IN {note_ids}")
        conn.commit()
    conn.close()
