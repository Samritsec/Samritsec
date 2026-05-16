import sqlite3
import os
from pathlib import Path
from datetime import datetime
from core.config.loader import ConfigLoader

class AuditLogger:
    """
    Tamper-evident (in future iterations) logging system for tracking all
    actions taken by the AI or tools within the NOVA ecosystem.
    """
    def __init__(self):
        # Resolve path from config or fallback to ~/.nova/audit.db
        config_path = ConfigLoader.get("paths", "db_path", "~/.nova/memory.db")
        # Keep audit log adjacent to main memory db
        base_dir = Path(os.path.expanduser(config_path)).parent
        self.db_path = base_dir / "audit.db"

        self._ensure_directories()
        self._init_db()

    def _ensure_directories(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    caller TEXT,
                    action_type TEXT,
                    target TEXT,
                    status TEXT,
                    details TEXT
                )
            ''')
            conn.commit()

    def log_action(self, caller: str, action_type: str, target: str, status: str, details: str = ""):
        """
        Logs a specific action.
        - caller: 'USER', 'AI_ORCHESTRATOR', 'SYS_TOOL'
        - action_type: 'EXECUTE', 'DELETE', 'MODIFY', 'NETWORK'
        - target: Filepath, IP address, or command executed
        - status: 'SUCCESS', 'FAILED', 'DENIED_BY_POLICY'
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO audit_logs (caller, action_type, target, status, details)
                VALUES (?, ?, ?, ?, ?)
            ''', (caller, action_type, target, status, details))
            conn.commit()

    def get_recent_logs(self, limit=50):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT timestamp, caller, action_type, target, status, details
                FROM audit_logs
                ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            return cursor.fetchall()

# Global instance
audit_logger = AuditLogger()
