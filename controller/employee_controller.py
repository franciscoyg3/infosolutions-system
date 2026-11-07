import sqlite3
from model.employee_model import EmployeeModel

class EmployeeController:
    def __init__(self, db, view):
        self.db = db
        self.view = view

    def add_employee(self):
        try:
            name, position, base_salary, bonus = self.view.ask_employee_data()
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
        except ValueError as error:
            self.view.show_message(f"Invalid data in the database: {error}")
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def show_payroll(self):
        try:
            total = EmployeeModel.calculate_payroll(self.db)
            self.view.show_message(f"Total payroll: {total:.2f} Kz")
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def show_highest_paid(self):
        try:
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
        except sqlite3.Error as error:
            self.view.show_message(f"Database error: {error}")

    def run(self):
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