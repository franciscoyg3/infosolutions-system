from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(exist_ok=True)

class Database:
    def __init__(self, filename="infosolutions.db"):
        self.filename = filename
        self.create_tables()

    def connect(self):
        con = sqlite3.connect(DB_DIR / self.filename)
        con.execute("PRAGMA foreign_keys = ON")
        return con

    def create_tables(self):
        with self.connect() as con:
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
                    total REAL NOT NULL,
                    sale_date TEXT NOT NULL,
                    FOREIGN KEY (customer_id) REFERENCES customers(id),
                    FOREIGN KEY (product_id) REFERENCES products(id)
                );
            """)