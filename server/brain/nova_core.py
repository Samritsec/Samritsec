import sqlite3
import os
from pathlib import Path
from cryptography.fernet import Fernet

DB_PATH = Path(__file__).parent.parent / "data" / "nova_core.db"
KEY_PATH = Path(__file__).parent.parent / "data" / "encryption.key"

class MemoryManager:
    def __init__(self):
        self.db_path = DB_PATH
        self.key = self._load_or_create_key()
        self.cipher = Fernet(self.key)
        self.init_db()

    def _load_or_create_key(self):
        if KEY_PATH.exists():
            return KEY_PATH.read_bytes()
        else:
            key = Fernet.generate_key()
            KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
            KEY_PATH.write_bytes(key)
            return key

    def encrypt(self, text: str) -> bytes:
        return self.cipher.encrypt(text.encode('utf-8'))

    def decrypt(self, token: bytes) -> str:
        return self.cipher.decrypt(token).decode('utf-8')

    def init_db(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE,
                    value BLOB
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    speaker TEXT,
                    message BLOB
                )
            ''')
            conn.commit()

    def save_preference(self, key: str, value: str):
        encrypted_val = self.encrypt(value)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO preferences (key, value)
                VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value=excluded.value
            ''', (key, encrypted_val))
            conn.commit()

    def save_conversation(self, speaker: str, message: str):
        encrypted_msg = self.encrypt(message)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO conversations (speaker, message)
                VALUES (?, ?)
            ''', (speaker, encrypted_msg))
            conn.commit()

    def get_recent_conversations(self, limit=10):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT speaker, message FROM conversations
                ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            rows = cursor.fetchall()

            history = []
            for speaker, enc_msg in reversed(rows):
                history.append((speaker, self.decrypt(enc_msg)))
            return history

# Global instance
memory = MemoryManager()
