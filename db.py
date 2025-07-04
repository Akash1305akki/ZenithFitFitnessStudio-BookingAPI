# booking_api/db.py
import sqlite3
from contextlib import contextmanager

DB_NAME = "fitness.db"

def init_db():
    """Initializes the SQLite database file if not present."""
    conn = sqlite3.connect(DB_NAME)
    conn.close()

@contextmanager
def get_db():
    """Provides a database connection using context manager."""
    conn = sqlite3.connect(DB_NAME)
    try:
        yield conn
    finally:
        conn.close()
