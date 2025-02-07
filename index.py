from flask import Flask, request, jsonify
import uuid
import time
import sqlite3

app = Flask(__name__)

DB_FILE = "database.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS keys (key TEXT, expires_at INTEGER)")
    conn.commit()
    conn.close()

@app.route("/api/generate", methods=["GET"])
def generate_key():
    new_key = str(uuid.uuid4())
    expires_at = int(time.time()) + 3600  # Berlaku 1 jam
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO keys (key, expires_at) VALUES (?, ?)", (new_key, expires_at))
    conn.commit()
    conn.close()
    return jsonify({"key": new_key, "expires_at": expires_at})

@app.route("/api/check", methods=["GET"])
def check_key():
    key = request.args.get("key")
    if not key:
        return jsonify({"error": "Key required"}), 400

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT expires_at FROM keys WHERE key = ?", (key,))
    result = cursor.fetchone()
    conn.close()

    if result:
        expires_at = result[0]
        if expires_at > time.time():
            return jsonify({"valid": True, "expires_at": expires_at})
        else:
            return jsonify({"valid": False, "error": "Expired"}), 400
    return jsonify({"valid": False, "error": "Not found"}), 404

if __name__ == "__main__":
    init_db()
    app.run()
