import sqlite3
import datetime
from keygen import generate_api_key, hash_key

DB_NAME = "myapi.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_name TEXT NOT NULL,
            hashed_key TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            request_count INTEGER DEFAULT 0,
            daily_limit INTEGER DEFAULT 100
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS request_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hashed_key TEXT NOT NULL,
            endpoint TEXT,
            timestamp TEXT NOT NULL,
            response_status TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hashed_key TEXT NOT NULL,
            user_message TEXT NOT NULL,
            ai_response TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')

    guest_key = "myapi-guestkey2024defaultaccess"
    hashed = hash_key(guest_key)
    cursor.execute('''
        INSERT OR IGNORE INTO api_keys
        (key_name, hashed_key, created_at, daily_limit)
        VALUES (?, ?, ?, ?)
    ''', ("guest-key", hashed, "2024-01-01", 99999))

    conn.commit()
    conn.close()


def create_api_key(key_name, daily_limit=100):
    api_key = generate_api_key()
    hashed = hash_key(api_key)
    created_at = datetime.datetime.now().isoformat()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO api_keys
        (key_name, hashed_key, created_at, daily_limit)
        VALUES (?, ?, ?, ?)
    ''', (key_name, hashed, created_at, daily_limit))
    conn.commit()
    conn.close()
    return api_key


def validate_api_key(api_key):
    hashed = hash_key(api_key)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, key_name, is_active, request_count, daily_limit
        FROM api_keys WHERE hashed_key = ?
    ''', (hashed,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return False, "Invalid API key"
    if row[2] == 0:
        return False, "API key is disabled"
    if row[3] >= row[4]:
        return False, "Daily limit reached"
    return True, row[1]


def increment_request_count(api_key, endpoint, status):
    hashed = hash_key(api_key)
    timestamp = datetime.datetime.now().isoformat()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE api_keys SET request_count = request_count + 1
        WHERE hashed_key = ?
    ''', (hashed,))
    cursor.execute('''
        INSERT INTO request_logs
        (hashed_key, endpoint, timestamp, response_status)
        VALUES (?, ?, ?, ?)
    ''', (hashed, endpoint, timestamp, status))
    conn.commit()
    conn.close()


def save_chat_history(api_key, user_message, ai_response):
    hashed = hash_key(api_key)
    timestamp = datetime.datetime.now().isoformat()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chat_history
        (hashed_key, user_message, ai_response, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (hashed, user_message, ai_response, timestamp))
    conn.commit()
    conn.close()


def get_chat_history(api_key, limit=10):
    hashed = hash_key(api_key)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT user_message, ai_response
        FROM chat_history WHERE hashed_key = ?
        ORDER BY id DESC LIMIT ?
    ''', (hashed, limit))
    rows = cursor.fetchall()
    conn.close()
    return rows[::-1]


def list_all_keys():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, key_name, created_at,
        is_active, request_count, daily_limit
        FROM api_keys
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_api_key(api_key):
    hashed = hash_key(api_key)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM api_keys WHERE hashed_key = ?', (hashed,))
    conn.commit()
    conn.close()


def reset_daily_counts():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE api_keys SET request_count = 0')
    conn.commit()
    conn.close()
