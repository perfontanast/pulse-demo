import os
import sqlite3
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

DB_FILE = f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/{os.getenv('DB_FILE')}"
DB_CONNECTION = sqlite3.connect(DB_FILE)
DB_CURSOR = DB_CONNECTION.cursor()


def query(sql: str, param: Optional[list] = None, commit: bool = True) -> list:
    if param is None:
        DB_CURSOR.execute(sql)
    else:
        DB_CURSOR.executemany(sql, param)
    if commit:
        DB_CONNECTION.commit()
    return DB_CURSOR.fetchall()


def init_db():
    """Initialize db."""
    query(
        'CREATE TABLE IF NOT EXISTS ohlc_data'
        # ticker denormalized for simplicity
        ' (ticker TEXT NOT NULL, ts NUMERIC, price NUMERIC NOT NULL,'
        ' PRIMARY KEY (ticker, ts))'
    )
    query('CREATE INDEX IF NOT EXISTS idx_ticker ON ohlc_data (ticker)')
    query('CREATE INDEX IF NOT EXISTS idx_ts ON ohlc_data (ts)')


if __name__ == '__main__':
    init_db()
