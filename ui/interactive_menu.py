
class InteractiveMenu:

    @staticmethod
    def display_main_menu():
        print("\n=== GAMBLING APP ===")
        print("1. Start Session")
        print("2. Place Bet")
        print("3. Show Status")
        print("4. End Session")
        print("5. Exit")

    @staticmethod
    def get_choice():
        try:
            return int(input("Enter choice: "))
        except:
            print("Invalid input")
            return None

    @staticmethod
    def prompt_bet_amount():
        try:
            return float(input("Enter bet amount: "))
        except:
            print("Invalid amount")
            return None