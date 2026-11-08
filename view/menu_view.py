class MenuView:
    @staticmethod
    def main_menu():
        print("---------------MAIN MENU---------------")
        print("0 - Exit System")
        print("1 - Customer Management")
        print("2 - Employee Management")
        print("3 - Product Management")
        print("4 - Sales Registration")
        print("5 - Reports")
        print(".....................................")
        # strip() so stray spaces still match the controller's string comparisons.
        return input("What would you like to do? : ").strip()

    @staticmethod
    def show_message(msg):
        print(msg)