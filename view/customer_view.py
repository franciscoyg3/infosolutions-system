class CustomerView:
    @staticmethod
    def menu():
        print("---------------CUSTOMER MENU---------------")
        print("0 - Back")
        print("1 - Add Customer")
        print("2 - List Customers")
        print("3 - Search Customer")
        print("4 - Update Customer")
        print("5 - Remove Customer")
        print(".....................................")
        return input("What would you like to do? : ").strip()

    @staticmethod
    def ask_customer_data():
        name = input("Enter the customer's name: ")
        phone = input("Enter the customer's phone number: ")
        email = input("Enter the customer's email: ")
        tax_id = input("Enter the customer's tax ID: ")
        return name, phone, email, tax_id

    @staticmethod
    def show_list(customers):
        if len(customers) < 1:
            print("No customers registered.")
            return

        for c in customers:
            print(f"{c.id} - Name: {c.name}, Phone: {c.phone}, Email: {c.email}, Tax ID: {c.tax_id}")

    @staticmethod
    def ask_search_term():
        return input("Enter a name or tax ID to search for the customer: ")

    @staticmethod
    def ask_id():
        return int(input("Enter the customer's ID: "))

    @staticmethod
    def show_message(msg):
        print(msg)