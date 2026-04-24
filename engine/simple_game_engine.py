from ui.game_status_display import GameStatusDisplay
from ui.interactive_menu import InteractiveMenu
from ui.session_summary import SessionSummary
from services.session_service import SessionService
from strategies.fixed_strategy import FixedAmountStrategy
from models.session_parameters import SessionParameters
from services.betting_service import BettingService
from repositories.gambler_repository import GamblerRepository

class SimpleGameEngine:
    def __init__(self, gambler):
        self.gambler = gambler
        self.session = None
        self.strategy = FixedAmountStrategy(100)

    def run(self):
        while True:
            InteractiveMenu.display_main_menu()
            choice = InteractiveMenu.get_choice()

            if choice == 1:
                self.session = SessionService.start_session(self.gambler.gambler_id)
                print("Session started")
            elif choice == 2:
                if not self.session:
                    print("Start a session first")
                    continue
                amount = InteractiveMenu.prompt_bet_amount()
                if not amount:
                    continue
                try:
                    result = BettingService.place_bet(
                        self.gambler.gambler_id,
                        amount,
                        self.session.session_id
                    )

                    GameStatusDisplay.display_game_outcome(result)
                except Exception as e:
                    print(f"Error: {e}")
            elif choice == 3:
                self.gambler = GamblerRepository.find_by_id(self.gambler.gambler_id)
                GameStatusDisplay.display_current_status(self.gambler)
            elif choice == 4:
                print("Session ended")
                break
            elif choice == 5:
                print("Exiting...")
                break
            else:
                print("Invalid choice")
