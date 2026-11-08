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
            # The model is expected to check stock, decrement it and insert the
            # sale in a single transaction. If any step fails, nothing should be
            # committed, otherwise stock and sales could drift apart.
            sale.register_sale(self.db)
            # sale.total is filled in by register_sale (price looked up at sale
            # time), so it is only available after the call above succeeds.
            self.view.show_message(f"Sale registered successfully. Total: {sale.total:.2f} Kz")
        except ValueError as error:
            self.view.show_message(f"Invalid input: {error}")
        # Business-rule error (not a DB error), so it is handled separately to
        # give the user a clear message. If InsufficientStockError subclasses
        # ValueError, this branch is unreachable because the handler above
        # catches it first; in that case, move it before the ValueError handler.
        except InsufficientStockError as error:
            self.view.show_message(f"Insufficient stock: {error}")
        # FK violation: customer_id or product_id doesn't exist. Only fires if
        # PRAGMA foreign_keys = ON; otherwise the model must check existence
        # itself. The message can't tell which of the two is missing.
        except sqlite3.IntegrityError:
            self.view.show_message("Customer or product does not exist.")
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def run(self):
        # Errors are handled per action; Ctrl+C/Ctrl+D propagate to AppController.
        while True:
            option = self.view.menu()
            if option == "1":
                self.register_sale()
            elif option == "0":
                break
            else:
                self.view.show_message("Invalid option.")