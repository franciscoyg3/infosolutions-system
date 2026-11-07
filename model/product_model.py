class ProductModel:
    def __init__(self, name, price, quantity, id=None):
        name = name.strip()
        if not name:
            raise ValueError("Invalid product name.")
        if price < 0:
            raise ValueError("Invalid price.")
        if quantity < 0:
            raise ValueError("Invalid quantity.")

        self.id, self.name = id, name
        self.price, self.quantity = price, quantity

    def add_product(self, db):
        with db.connect() as con:
            cur = con.execute(
                "INSERT INTO products (name, price, quantity) VALUES (?,?,?)",
                (self.name, self.price, self.quantity)
            )
            self.id = cur.lastrowid

    @staticmethod
    def remove_product(db, id):
        with db.connect() as con:
            cur = con.execute(
                "DELETE FROM products WHERE id=?",
                (id,)
            )
            if cur.rowcount == 0:
                raise ValueError("Product not found.")

    @staticmethod
    def list_products(db):
        with db.connect() as con:
            rows = con.execute(
                "SELECT id, name, price, quantity FROM products"
            ).fetchall()
        return [ProductModel(n, p, q, id) for id, n, p, q in rows]

    @staticmethod
    def update_stock(db, id, new_quantity):
        if new_quantity < 0:
            raise ValueError("Invalid quantity.")
        with db.connect() as con:
            cur = con.execute(
                "UPDATE products SET quantity=? WHERE id=?",
                (new_quantity, id)
            )
            if cur.rowcount == 0:
                raise ValueError("Product not found.")