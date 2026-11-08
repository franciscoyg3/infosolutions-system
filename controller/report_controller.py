import sqlite3
from model.customer_model import CustomerModel
from model.employee_model import EmployeeModel
from model.sale_model import SaleModel


class ReportController:
    def __init__(self, db, view):
        self.db = db
        self.view = view

    def customer_report(self):
        try:
            customers = CustomerModel.list_customers(self.db)
            if customers:
                self.view.show_customers(customers)
            else:
                self.view.show_message("No customers registered.")
        # Rows are rebuilt as CustomerModel instances, so ValueError means bad
        # data already in the DB. Other reports have no such handler because
        # they don't go through model validation.
        except ValueError as error:
            self.view.show_message(f"Invalid data in the database: {error}")
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def sales_report(self):
        try:
            sales = SaleModel.list_sales(self.db)
            if sales:
                self.view.show_sales(sales)
            else:
                self.view.show_message("No sales registered.")
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def best_selling_product_report(self):
        try:
            # Returns a (name, quantity) tuple, or None when there are no sales
            # (an aggregate with LIMIT 1 yields no row). On ties, only one
            # product is returned, and which one depends on the query's ordering.
            result = SaleModel.best_selling_product(self.db)
            if result:
                name, quantity = result
                self.view.show_message(f"Best-selling product: {name} ({quantity} units)")
            else:
                self.view.show_message("No sales registered.")
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def top_customer_report(self):
        try:
            # Same contract as best_selling_product: (name, total) or None.
            result = SaleModel.top_customer(self.db)
            if result:
                name, total = result
                self.view.show_message(f"Top customer: {name} (total spent: {total:.2f} Kz)")
            else:
                self.view.show_message("No sales registered.")
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def total_sales_report(self):
        try:
            # Unlike the reports above, there is no empty check: this assumes the
            # model returns 0 for an empty table. A bare SQL SUM() returns NULL
            # (None) there, and :.2f would raise a TypeError that isn't caught
            # here. The model should use COALESCE(SUM(...), 0).
            total = SaleModel.total_sales(self.db)
            self.view.show_message(f"Total sales: {total:.2f} Kz")
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def highest_salary_report(self):
        try:
            # Returns a list so that ties for the top salary are all shown.
            employees = EmployeeModel.get_highest_paid(self.db)
            if employees:
                self.view.show_highest_paid(employees)
            else:
                self.view.show_message("No employees registered.")
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def payroll_report(self):
        try:
            # Same empty-table caveat as total_sales_report.
            total = EmployeeModel.calculate_payroll(self.db)
            self.view.show_message(f"Total payroll: {total:.2f} Kz")
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def run(self):
        # Errors are handled per report; Ctrl+C/Ctrl+D propagate to AppController.
        while True:
            option = self.view.menu()
            if option == "1":
                self.customer_report()
            elif option == "2":
                self.sales_report()
            elif option == "3":
                self.best_selling_product_report()
            elif option == "4":
                self.top_customer_report()
            elif option == "5":
                self.total_sales_report()
            elif option == "6":
                self.highest_salary_report()
            elif option == "7":
                self.payroll_report()
            elif option == "0":
                break
            else:
                self.view.show_message("Invalid option.")