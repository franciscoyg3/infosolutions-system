class SaleView:
    @staticmethod
    def menu():
        print("---------------SALES MENU---------------")
        print("0 - Back")
        print("1 - Register Sale")
        print(".....................................")
        return input("What would you like to do? : ").strip()

    @staticmethod
    def ask_sale_data():
        while True:
            try:
                customer_id = int(input("Enter the customer's ID: "))
                product_id = int(input("Enter the product's ID: "))
                quantity = int(input("Enter the sale quantity: "))
                return customer_id, product_id, quantity
            except ValueError:
                print("Invalid input. Please enter whole numbers only.")

    @staticmethod
    def show_message(msg):
        print(msg)