class ProductView:
    @staticmethod
    def menu():
        print("---------------PRODUCT MENU---------------")
        print("0 - Back")
        print("1 - Add Product")
        print("2 - List Products")
        print("3 - Update Stock")
        print("4 - Remove Product")
        print(".....................................")
        # strip() removes stray spaces so the option matches the controller's string comparisons
        return input("What would you like to do? : ").strip()

    @staticmethod
    def ask_product_data():
        name = input("Enter the product's name: ")
        # Price is read as a decimal number, quantity as a whole number
        price = float(input("Enter the product's price: "))
        quantity = int(input("Enter the product's quantity: "))
        return name, price, quantity

    @staticmethod
    def show_list(products):
        # Handles the empty case here, so the controller can pass the list straight through
        if len(products) < 1:
            print("No products registered.")
            return

        for p in products:
            print(f"{p.id} - Name: {p.name}, Price: {p.price:.2f} Kz, Quantity: {p.quantity}")

    @staticmethod
    def ask_id():
        # Keeps asking until the input converts to an int, then returns it
        while True:
            try:
                return int(input("Enter the product's ID: "))
            except ValueError:
                print("Invalid ID. Please enter a number.")

    @staticmethod
    def ask_stock():
        # Keeps asking until the input converts to an int, then returns it
        while True:
            try:
                return int(input("Enter the product's new stock quantity: "))
            except ValueError:
                print("Invalid quantity. Please enter a whole number.")

    @staticmethod
    def show_message(msg):
        print(msg)