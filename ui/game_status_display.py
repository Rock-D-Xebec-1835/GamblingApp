
class GameStatusDisplay:

    @staticmethod
    def display_current_status(gambler):
        print("\n--- CURRENT STATUS ---")
        print(f"Balance: {gambler.current_balance}")
        print(f"Total Bets: {gambler.total_bets}")
        print(f"Total Winnings: {gambler.total_winnings}")

    @staticmethod
    def display_game_outcome(game_result):
        print("\n--- GAME RESULT ---")
        print(game_result)