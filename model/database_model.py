from pathlib import Path
import sqlite3

# Project root is two levels above this file (this file lives in model/)
BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "database"
# Runs at import time, so the folder exists before the first connection
DB_DIR.mkdir(exist_ok=True)

class DatabaseModel:
    def __init__(self, filename="infosolutions.db"):
        self.filename = filename
        # Schema is created on instantiation, so the app can start on an empty folder
        self.create_tables()

    def connect(self):
        # Opens a new connection on every call; callers use it as a context manager
        con = sqlite3.connect(DB_DIR / self.filename)
        # SQLite ignores foreign keys by default and the setting is per connection,
        # so it is enabled on each one here
        con.execute("PRAGMA foreign_keys = ON")
        return con

    def create_tables(self):
        with self.connect() as con:
            # executescript runs all the statements in one call;
            # IF NOT EXISTS makes it safe to run on every startup
            con.executescript("""
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT,
                    tax_id TEXT UNIQUE
                );
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    position TEXT,
                    base_salary REAL NOT NULL,
                    bonus REAL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    quantity INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    -- total is stored at sale time, so later price changes don't alter past sales
                    total REAL NOT NULL,
                    sale_date TEXT NOT NULL,
                    -- these keys block deleting a customer or product that has sales
                    FOREIGN KEY (customer_id) REFERENCES customers(id),
                    FOREIGN KEY (product_id) REFERENCES products(id)
                );
            """)