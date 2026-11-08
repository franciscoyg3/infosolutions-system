import sqlite3
from model.customer_model import CustomerModel

class CustomerController:
    def __init__(self, db, view):
        self.db = db
        self.view = view

    def add_customer(self):
        try:
            name, phone, email, tax_id = self.view.ask_customer_data()
            # Validation lives in the model constructor; invalid data raises
            # ValueError before anything touches the database.
            customer = CustomerModel(name, phone, email, tax_id)
            customer.add_customer(self.db)
            self.view.show_message("Customer added successfully.")
        except ValueError as error:
            self.view.show_message(f"Invalid input: {error}")
        # Order matters: IntegrityError is a subclass of sqlite3.Error, so it
        # must come first or the generic handler would swallow it.
        # Assumes a UNIQUE constraint on tax_id in the schema.
        except sqlite3.IntegrityError:
            self.view.show_message("A customer with this tax ID already exists.")
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def list_customers(self):
        try:
            self.view.show_list(CustomerModel.list_customers(self.db))
        # Rows are rebuilt as CustomerModel instances, so ValueError here means
        # corrupted/legacy data in the DB, not bad user input.
        except ValueError as error:
            self.view.show_message(f"Invalid data in the database: {error}")
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def search_customer(self):
        try:
            term = self.view.ask_search_term()
            customers = CustomerModel.search_customer(self.db, term)
            if customers:
                self.view.show_list(customers)
            else:
                self.view.show_message("No customers found.")
        except ValueError as error:
            self.view.show_message(f"Invalid input: {error}")
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def update_customer(self):
        try:
            id = self.view.ask_id()
            name, phone, email, tax_id = self.view.ask_customer_data()
            CustomerModel.update_customer(self.db, id, name, phone, email, tax_id)
            self.view.show_message("Customer updated successfully.")
        except ValueError as error:
            self.view.show_message(f"Invalid input: {error}")
        # On update, the UNIQUE violation means the new tax_id collides with a
        # *different* customer (the row's own value doesn't conflict with itself).
        except sqlite3.IntegrityError:
            self.view.show_message("This tax ID already belongs to another customer.")
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def remove_customer(self):
        try:
            id = self.view.ask_id()
            CustomerModel.remove_customer(self.db, id)
            self.view.show_message("Customer removed successfully.")
        except ValueError as error:
            self.view.show_message(f"Invalid input: {error}")
        # Foreign key violation from the sales table. SQLite only enforces FKs
        # if PRAGMA foreign_keys = ON was set on this connection; otherwise
        # this branch never fires and orphaned sales are silently created.
        except sqlite3.IntegrityError:
            self.view.show_message("Cannot remove: the customer has registered sales.")
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def run(self):
        # No try/except here on purpose: each action handles its own errors,
        # and Ctrl+C/Ctrl+D bubble up to AppController.run, which exits cleanly.
        while True:
            option = self.view.menu()
            if option == "1":
                self.add_customer()
            elif option == "2":
                self.list_customers()
            elif option == "3":
                self.search_customer()
            elif option == "4":
                self.update_customer()
            elif option == "5":
                self.remove_customer()
            elif option == "0":
                break
            else:
                self.view.show_message("Invalid option.")