import sqlite3
from datetime import datetime
from typing import List, Optional, Tuple

class Database:
    def __init__(self, db_path="math_requests.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    op_type TEXT NOT NULL,
                    operands TEXT NOT NULL,
                    result INTEGER,
                    timestamp TEXT NOT NULL
                )
            ''')
            conn.commit()

    def save_request(self, op_type: str, operands: List[int], result: int):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                'INSERT INTO requests (op_type, operands, result, timestamp) VALUES (?, ?, ?, ?)',
                (op_type, str(operands), result, datetime.utcnow().isoformat())
            )
            conn.commit()

    def fetch_all_requests(self) -> List[Tuple]:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT op_type, operands, result, timestamp FROM requests ORDER BY timestamp DESC')
            return c.fetchall()
