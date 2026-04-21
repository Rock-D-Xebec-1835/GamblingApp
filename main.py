from db.db_manager import DBManager
from services.gambler_service import GamblerService

def test_connection():
    result = DBManager.fetch_one("SELECT DATABASE() as db")
    print("Connected to:", result["db"])


# TEST GAMBLER
def testGambler():
    gambler = GamblerService.create_gambler(
        name="Sindhur",
        initial_balance=1000,
        win_threshold=2000,
        loss_threshold=500
    )

    print("Created ID: ", gambler.gambler_id)
    fetched = GamblerService.get_gambler(gambler.gambler_id)
    print("Name: ", fetched.name)
    print("Current Stake: ", fetched.current_balance)
    print("Total Bets: ", fetched.total_bets)
    print("Minimum Stake: ", fetched.min_balance)


if __name__ == "__main__":
    test_connection()
    testGambler()