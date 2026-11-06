from pathlib import Path
import sqlite3
base_dir = Path(__file__).resolve().parent.parent
BD_dir = base_dir / "database"
BD_dir.mkdir(exist_ok=True)

class Database:
  def __init__(self, ficheiro="infosolutions.db"):
    self.ficheiro = ficheiro
    self.criar_tabelas()

  def ligar(self):
    con = sqlite3.connect(BD_dir / self.ficheiro)
    con.execute("PRAGMA foreign_keys = on")
    return con

  def criar_tabelas(self):
    with self.ligar() as con:
      con.executescript("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT NOT NULL,
                email TEXT,
                nif TEXT UNIQUE
            );
            CREATE TABLE IF NOT EXISTS funcionarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL, cargo TEXT,
                salario_base REAL NOT NULL, bonus REAL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL, quantidade INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                produto_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                total REAL NOT NULL,
                data TEXT NOT NULL,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id),
                FOREIGN KEY (produto_id) REFERENCES produtos(id)
            );
            """)