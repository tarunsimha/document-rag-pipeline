import sqlite3

conn = sqlite3.connect("metadata_db.db")
cur = conn.cursor()

def create_table():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT NOT NULL UNIQUE,
        filename TEXT NOT NULL,
        extension TEXT,
        size INTEGER,
        modified REAL,
        file_type TEXT
    )
    """)

def add_to_db(file_attrs):
    cur.execute("""
    INSERT INTO files (path, filename, extension, size, modified, file_type)
    VALUES (?, ?, ?, ?, ?, ?)

    ON CONFLICT(path)
    DO UPDATE SET
        filename  = excluded.filename,
        extension = excluded.extension,
        size = excluded.size,
        modified = excluded.modified,
        file_type = excluded.file_type
    """, (
        file_attrs["path"],
        file_attrs["filename"],
        file_attrs["extension"],
        file_attrs["size"],
        file_attrs["modified"],
        file_attrs["file_type"]
    ))
    
def debug_data():
    cur.execute("SELECT * FROM files WHERE extension='pdf';")
    return cur.fetchall()

def commit_changes():
    conn.commit()

def close_db():
    conn.close()