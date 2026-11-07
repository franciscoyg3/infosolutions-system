import re

class CustomerModel:
    def __init__(self, name, phone, email, tax_id, id=None):
        name = name.strip()
        phone = self.normalize_phone(phone)
        email = email.strip()
        tax_id = str(tax_id).strip().upper()

        if not name:
            raise ValueError("Name cannot be empty.")
        if not self.is_valid_email(email):
            raise ValueError("Invalid email.")
        if not self.is_valid_tax_id(tax_id):
            raise ValueError("Invalid tax ID.")
        if not self.is_valid_phone(phone):
            raise ValueError("Invalid phone number.")

        self.id, self.name, self.phone = id, name, phone
        self.email, self.tax_id = email, tax_id

    @staticmethod
    def normalize_phone(phone):
        """Remove spaces, dashes and the +244 / 00244 prefix."""
        p = re.sub(r"[\s\-]", "", str(phone))
        if p.startswith("+244"):
            p = p[4:]
        elif p.startswith("00244"):
            p = p[5:]
        return p

    @staticmethod
    def is_valid_phone(phone):
        """Mobile (9 + 8 digits) or landline (22 + 7 digits)."""
        return re.match(r"^(22|9\d)\d{7}$", phone) is not None

    @staticmethod
    def is_valid_email(email):
        """Basic email format validation."""
        return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) is not None

    @staticmethod
    def is_valid_tax_id(tax_id):
        """Company tax ID (10 digits starting with 5) or national ID card format."""
        return re.match(r"^(5\d{9}|\d{9}[A-Z]{2}\d{3})$", tax_id) is not None

    def add_customer(self, db):
        with db.connect() as con:
            cur = con.execute(
                "INSERT INTO customers (name, phone, email, tax_id) VALUES (?,?,?,?)",
                (self.name, self.phone, self.email, self.tax_id)
            )
            self.id = cur.lastrowid

    @staticmethod
    def remove_customer(db, id):
        with db.connect() as con:
            cur = con.execute(
                "DELETE FROM customers WHERE id=?", (id,)
            )
            if cur.rowcount == 0:
                raise ValueError("Customer not found.")

    @staticmethod
    def list_customers(db):
        with db.connect() as con:
            rows = con.execute(
                "SELECT id, name, phone, email, tax_id FROM customers"
            ).fetchall()
        return [CustomerModel(n, p, e, t, id) for id, n, p, e, t in rows]

    @staticmethod
    def update_customer(db, id, name, phone, email, tax_id):
        c = CustomerModel(name, phone, email, tax_id, id)
        with db.connect() as con:
            cur = con.execute(
                "UPDATE customers SET name=?, phone=?, email=?, tax_id=? WHERE id=?",
                (c.name, c.phone, c.email, c.tax_id, id)
            )
            if cur.rowcount == 0:
                raise ValueError("Customer not found.")

    @staticmethod
    def search_customer(db, term):
        term = term.strip()
        if not term:
            raise ValueError("Enter a name or tax ID to search.")

        with db.connect() as con:
            rows = con.execute(
                "SELECT id, name, phone, email, tax_id FROM customers "
                "WHERE name LIKE ? OR tax_id=?",
                (f"%{term}%", term)
            ).fetchall()

        return [CustomerModel(n, p, e, t, id) for id, n, p, e, t in rows]