class ReportView:
    @staticmethod
    def menu():
        print("---------------REPORTS MENU---------------")
        print("0 - Back")
        print("1 - Customer Report")
        print("2 - Sales Report")
        print("3 - Best-Selling Product Report")
        print("4 - Top Customer Report")
        print("5 - Total Sales Report")
        print("6 - Highest Salary Report")
        print("7 - Payroll Report")
        print(".....................................")
        return input("What would you like to do? : ").strip()

    @staticmethod
    def show_customers(customers):
        for c in customers:
            print(f"{c.id} - Name: {c.name}, Phone: {c.phone}, Email: {c.email}, Tax ID: {c.tax_id}")

    @staticmethod
    def show_message(msg):
        print(msg)

    @staticmethod
    def show_sales(sales):
        for id, customer, product, quantity, total, sale_date in sales:
            print(
                f"{id} - Customer: {customer}, Product: {product}, "
                f"Quantity: {quantity}, Total: {total:.2f} Kz, Date: {sale_date}"
            )

    @staticmethod
    def show_highest_paid(employees):
        for e in employees:
            print(f"{e.id} - {e.name} ({e.position}), Total Salary: {e.total_salary:.2f} Kz.")