from controller.customer_controller import CustomerController
from controller.employee_controller import EmployeeController
from controller.product_controller import ProductController
from controller.sale_controller import SaleController
from controller.report_controller import ReportController

from view.menu_view import MenuView
from view.customer_view import CustomerView
from view.employee_view import EmployeeView
from view.product_view import ProductView
from view.sale_view import SaleView
from view.report_view import ReportView

class AppController:
    """Main controller: shows the menu and delegates to each module."""

    def __init__(self, db):
        self.db = db
        self.view = MenuView()

        self.customers = CustomerController(db, CustomerView())
        self.employees = EmployeeController(db, EmployeeView())
        self.products = ProductController(db, ProductView())
        self.sales = SaleController(db, SaleView())
        self.reports = ReportController(db, ReportView())

    def run(self):
        """Main menu loop. It only ends when the user chooses 0."""
        while True:
            try:
                option = self.view.main_menu()
                if option == "1":
                    self.customers.run()
                elif option == "2":
                    self.employees.run()
                elif option == "3":
                    self.products.run()
                elif option == "4":
                    self.sales.run()
                elif option == "5":
                    self.reports.run()
                elif option == "0":
                    self.view.show_message("Exiting the system. See you soon!")
                    break
                else:
                    self.view.show_message("Invalid option.")
            except (KeyboardInterrupt, EOFError):
                self.view.show_message("\nSystem closed.")
                break
            except Exception as error:
                self.view.show_message(f"Unexpected error: {error}")