import sqlite3

DB_FILE = "database.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS keys (key TEXT, expires_at INTEGER)")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
