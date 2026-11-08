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

        # All controllers share the same db connection, while each gets its own
        # view instance. Injecting both keeps controllers testable with mocks.
        self.customers = CustomerController(db, CustomerView())
        self.employees = EmployeeController(db, EmployeeView())
        self.products = ProductController(db, ProductView())
        self.sales = SaleController(db, SaleView())
        self.reports = ReportController(db, ReportView())

    def run(self):
        """Main menu loop. It only ends when the user chooses 0."""
        while True:
            try:
                # input() returns str, so options are compared as strings
                # on purpose (no int() cast that could raise ValueError).
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
                # Ctrl+C / Ctrl+D: exit cleanly instead of dumping a traceback.
                # The leading \n moves the message off the line where ^C was echoed.
                self.view.show_message("\nSystem closed.")
                break
            except Exception as error:
                # Catch-all keeps the app alive if a single module fails, so the
                # user returns to the menu. Trade-off: the traceback is hidden,
                # so consider logging it here for debugging.
                self.view.show_message(f"Unexpected error: {error}")