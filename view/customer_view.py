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
        # strip() removes stray spaces so the option matches the controller's string comparisons
        return input("What would you like to do? : ").strip()

    @staticmethod
    def ask_customer_data():
        # Collects the four fields as plain strings, exactly as typed
        name = input("Enter the customer's name: ")
        phone = input("Enter the customer's phone number: ")
        email = input("Enter the customer's email: ")
        tax_id = input("Enter the customer's tax ID: ")
        return name, phone, email, tax_id

    @staticmethod
    def show_list(customers):
        # Handles the empty case here, so the controller can pass the list straight through
        if len(customers) < 1:
            print("No customers registered.")
            return

        for c in customers:
            print(f"{c.id} - Name: {c.name}, Phone: {c.phone}, Email: {c.email}, Tax ID: {c.tax_id}")

    @staticmethod
    def ask_search_term():
        # The same term is used to look up customers by name or by tax ID
        return input("Enter a name or tax ID to search for the customer: ")

    @staticmethod
    def ask_id():
        # Converts the input to an int, so non-numeric text raises ValueError to the caller
        return int(input("Enter the customer's ID: "))

    @staticmethod
    def show_message(msg):
        print(msg)