import sqlite3
from model.sale_model import SaleModel, InsufficientStockError


class SaleController:
    def __init__(self, db, view):
        self.db = db
        self.view = view

    def register_sale(self):
        try:
            customer_id, product_id, quantity = self.view.ask_sale_data()
            sale = SaleModel(customer_id, product_id, quantity)
            sale.register_sale(self.db)
            self.view.show_message(f"Sale registered successfully. Total: {sale.total:.2f} Kz")
        except ValueError as error:
            self.view.show_message(f"Invalid input: {error}")
        except InsufficientStockError as error:
            self.view.show_message(f"Insufficient stock: {error}")
        except sqlite3.IntegrityError:
            self.view.show_message("Customer or product does not exist.")
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def run(self):
        while True:
            option = self.view.menu()
            if option == "1":
                self.register_sale()
            elif option == "0":
                break
            else:
                self.view.show_message("Invalid option.")