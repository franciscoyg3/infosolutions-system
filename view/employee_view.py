class EmployeeView:
    @staticmethod
    def menu():
        print("---------------EMPLOYEE MENU---------------")
        print("0 - Back")
        print("1 - Add Employee")
        print("2 - List Employees")
        print("3 - Show Payroll")
        print("4 - Show Highest-Paid Employee")
        print("5 - Remove Employee")
        print(".....................................")
        # strip() removes stray spaces so the option matches the controller's string comparisons
        return input("What would you like to do? : ").strip()

    @staticmethod
    def ask_id():
        # Keeps asking until the input converts to an int, then returns it
        while True:
            try:
                return int(input("Enter the employee's ID: "))
            except ValueError:
                print("Invalid ID. Please enter a number.")

    @staticmethod
    def ask_employee_data():
        name = input("Enter the employee's name: ")
        position = input("Enter the employee's position: ")
        # Salary and bonus are read as decimal numbers
        base_salary = float(input("Enter the employee's base salary: "))
        bonus = float(input("Enter the employee's bonus: "))
        return name, position, base_salary, bonus

    @staticmethod
    def show_message(msg):
        print(msg)

    @staticmethod
    def show_list(employees):
        # Handles the empty case here, so the controller can pass the list straight through
        if len(employees) < 1:
            print("No employees registered.")
            return

        for e in employees:
            print(
                f"{e.id} - Name: {e.name}, Position: {e.position}, "
                f"Base Salary: {e.base_salary:.2f} Kz, Bonus: {e.bonus:.2f} Kz"
            )

    @staticmethod
    def show_highest_paid(employees):
        # Prints every employee in the list, since ties for the top salary are all shown
        for e in employees:
            print(f"{e.id} - {e.name} ({e.position}), Total Salary: {e.total_salary:.2f} Kz.")