from datetime import datetime

class InsufficientStockError(Exception):
    """Raised when trying to sell more units than are in stock."""

class SaleModel:
    def __init__(self, customer_id, product_id, quantity, total=0, sale_date="", id=None):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.id, self.customer_id = id, customer_id
        self.product_id, self.quantity = product_id, quantity
        self.total, self.sale_date = total, sale_date

    def register_sale(self, db):
        with db.connect() as con:
            product = con.execute(
                "SELECT price, quantity FROM products WHERE id=?",
                (self.product_id,)
            ).fetchone()
            if product is None:
                raise ValueError("Product not found.")

            price, stock = product
            if stock < self.quantity:
                raise InsufficientStockError(f"Available stock: {stock}.")

            self.total = self.quantity * price
            self.sale_date = datetime.now().strftime("%Y-%m-%d %H:%M")

            cur = con.execute(
                "INSERT INTO sales (customer_id, product_id, quantity, total, sale_date) "
                "VALUES (?,?,?,?,?)",
                (self.customer_id, self.product_id, self.quantity, self.total, self.sale_date)
            )
            self.id = cur.lastrowid

            con.execute(
                "UPDATE products SET quantity = quantity - ? WHERE id=?",
                (self.quantity, self.product_id)
            )

    @staticmethod
    def list_sales(db):
        """Return (id, customer, product, quantity, total, sale_date) for all sales."""
        with db.connect() as con:
            return con.execute("""
                SELECT s.id, c.name, p.name, s.quantity, s.total, s.sale_date
                FROM sales s
                JOIN customers c ON c.id = s.customer_id
                JOIN products p ON p.id = s.product_id
                ORDER BY s.id DESC
            """).fetchall()

    @staticmethod
    def total_sales(db):
        with db.connect() as con:
            return con.execute(
                "SELECT COALESCE(SUM(total), 0) FROM sales"
            ).fetchone()[0]

    @staticmethod
    def best_selling_product(db):
        with db.connect() as con:
            return con.execute("""
                SELECT p.name, SUM(s.quantity) AS total_sold
                FROM sales s
                JOIN products p ON p.id = s.product_id
                GROUP BY p.id
                ORDER BY total_sold DESC, p.name
                LIMIT 1
            """).fetchone()

    @staticmethod
    def top_customer(db):
        with db.connect() as con:
            return con.execute("""
                SELECT c.name, SUM(s.total) AS total_spent
                FROM sales s
                JOIN customers c ON c.id = s.customer_id
                GROUP BY c.id
                ORDER BY total_spent DESC, c.name
                LIMIT 1
            """).fetchone()