import sqlite3
from model.product_model import ProductModel


class ProductController:
    def __init__(self, db, view):
        self.db = db
        self.view = view

    def add_product(self):
        try:
            name, price, quantity = self.view.ask_product_data()
            # Price/quantity validation (e.g. non-negative) is expected in the
            # model constructor, so bad values never reach the DB.
            product = ProductModel(name, price, quantity)
            product.add_product(self.db)
            self.view.show_message("Product added successfully.")
        except ValueError as error:
            self.view.show_message(f"Invalid input: {error}")
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def list_products(self):
        try:
            self.view.show_list(ProductModel.list_products(self.db))
        except ValueError as error:
            self.view.show_message(f"Invalid data in the database: {error}")
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def update_stock(self):
        try:
            id = self.view.ask_id()
            new_quantity = self.view.ask_stock()
            # Sets the stock to an absolute value; it does not add to the current
            # one. Sales should decrement stock through SaleController instead,
            # otherwise manual edits here can race with or overwrite sale updates.
            ProductModel.update_stock(self.db, id, new_quantity)
            self.view.show_message("Stock updated successfully.")
        except ValueError as error:
            # Raised for a malformed or negative quantity, or an unknown product id
            # (depends on how the model reports a missing row).
            self.view.show_message(f"Invalid input: {error}")
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def remove_product(self):
        try:
            id = self.view.ask_id()
            ProductModel.remove_product(self.db, id)
            self.view.show_message("Product removed successfully.")
        except ValueError as error:
            self.view.show_message(f"Invalid input: {error}")
        # Foreign key violation from the sales table. Only fires if
        # PRAGMA foreign_keys = ON was set on this connection.
        except sqlite3.IntegrityError:
            self.view.show_message("Cannot remove: the product has registered sales.")
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def run(self):
        # Errors are handled per action; Ctrl+C/Ctrl+D propagate to AppController.
        while True:
            option = self.view.menu()
            if option == "1":
                self.add_product()
            elif option == "2":
                self.list_products()
            elif option == "3":
                self.update_stock()
            elif option == "4":
                self.remove_product()
            elif option == "0":
                break
            else:
                self.view.show_message("Invalid option.")