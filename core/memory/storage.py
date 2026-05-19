import sqlite3
import os
from pathlib import Path
from cryptography.fernet import Fernet
from core.config.loader import ConfigLoader

class MemoryStorage:
    def __init__(self):
        # Resolve path from config or fallback to ~/.nova/
        config_path = ConfigLoader.get("paths", "db_path", "~/.nova/memory.db")
        self.db_path = Path(os.path.expanduser(config_path))
        self.key_path = self.db_path.parent / "encryption.key"

        self._ensure_directories()
        self.key = self._load_or_create_key()
        self.cipher = Fernet(self.key)
        self._init_db()

    def _ensure_directories(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def _load_or_create_key(self):
        if self.key_path.exists():
            return self.key_path.read_bytes()
        else:
            key = Fernet.generate_key()
            self.key_path.write_bytes(key)
            # Ensure strict permissions on Linux
            os.chmod(self.key_path, 0o600)
            return key

    def encrypt(self, text: str) -> bytes:
        return self.cipher.encrypt(text.encode('utf-8'))

    def decrypt(self, token: bytes) -> str:
        return self.cipher.decrypt(token).decode('utf-8')

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversation_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    speaker TEXT,
                    message BLOB
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_knowledge (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE,
                    value BLOB
                )
            ''')
            conn.commit()

    def save_message(self, speaker: str, message: str):
        encrypted_msg = self.encrypt(message)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO conversation_history (speaker, message)
                VALUES (?, ?)
            ''', (speaker, encrypted_msg))
            conn.commit()

    def get_recent_messages(self, limit=10):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT speaker, message FROM conversation_history
                ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            rows = cursor.fetchall()

            history = []
            for speaker, enc_msg in reversed(rows):
                history.append((speaker, self.decrypt(enc_msg)))
            return history

# Global instance
memory = MemoryStorage()
