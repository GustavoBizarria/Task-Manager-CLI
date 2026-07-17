import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "tasks.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            priority TEXT NOT NULL DEFAULT 'medium',
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )
    conn.commit()
    conn.close()