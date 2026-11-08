import sqlite3
from model.employee_model import EmployeeModel

class EmployeeController:
    def __init__(self, db, view):
        self.db = db
        self.view = view

    def add_employee(self):
        try:
            name, position, base_salary, bonus = self.view.ask_employee_data()
            # Salary/bonus validation (e.g. non-negative values) is expected to
            # happen in the model constructor, raising ValueError before any DB write.
            employee = EmployeeModel(name, position, base_salary, bonus)
            employee.add_employee(self.db)
            self.view.show_message("Employee added successfully.")
        except ValueError as error:
            self.view.show_message(f"Invalid input: {error}")
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def list_employees(self):
        try:
            self.view.show_list(EmployeeModel.list_employees(self.db))
        # Rows are rebuilt through the model, so ValueError means bad data
        # already stored in the DB, not bad user input.
        except ValueError as error:
            self.view.show_message(f"Invalid data in the database: {error}")
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def show_payroll(self):
        try:
            # Aggregated in the model/SQL, so no per-row validation happens here;
            # that's why there is no ValueError handler in this method.
            total = EmployeeModel.calculate_payroll(self.db)
            self.view.show_message(f"Total payroll: {total:.2f} Kz")
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def show_highest_paid(self):
        try:
            # Returns a list (not a single employee) so that ties for the
            # highest salary are all shown. An empty list means no employees.
            employees = EmployeeModel.get_highest_paid(self.db)
            if employees:
                self.view.show_highest_paid(employees)
            else:
                self.view.show_message("No employees registered.")
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def remove_employee(self):
        try:
            id = self.view.ask_id()
            EmployeeModel.remove_employee(self.db, id)
            self.view.show_message("Employee removed successfully.")
        except ValueError as error:
            self.view.show_message(f"Invalid input: {error}")
        # No IntegrityError branch, unlike CustomerController: this assumes
        # sales don't reference employees via a foreign key. If they do, removal
        # would fall into the generic handler with a vague "Database error".
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def run(self):
        # Errors are handled per action; Ctrl+C/Ctrl+D propagate to AppController.
        while True:
            option = self.view.menu()
            if option == "1":
                self.add_employee()
            elif option == "2":
                self.list_employees()
            elif option == "3":
                self.show_payroll()
            elif option == "4":
                self.show_highest_paid()
            elif option == "5":
                self.remove_employee()
            elif option == "0":
                break
            else:
                self.view.show_message("Invalid option.")