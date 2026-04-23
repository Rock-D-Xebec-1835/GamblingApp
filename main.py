from db.db_manager import DBManager
from services.gambler_service import GamblerService
from services.stake_management_service import StakeManagementService
from services.betting_service import BettingService
from services.session_service import SessionService

def test_connection():
    result = DBManager.fetch_one("SELECT DATABASE() as db")
    print("Connected to:", result["db"])


# TEST GAMBLER
def testGambler():
    try:
        gambler = GamblerService.get_gambler(1)
        print("Using existing gambler:", gambler.gambler_id)
        return gambler
    except:
        gambler = GamblerService.create_gambler(
            name="Sindhur",
            initial_balance=1000,
            win_threshold=2000,
            loss_threshold=500
        )
        print("Created ID:", gambler.gambler_id)
        return gambler

# TEST STAKE
def testStake(gambler_id):
    print("\nDEPOSIT\n")
    g = StakeManagementService.deposit(gambler_id, 500)
    print("Balance after deposit: ", g.current_balance)
    print("\nWITHDRAWAL\n")
    g = StakeManagementService.withdraw(gambler_id, 500)
    print("Balance after withdrawal: ", g.current_balance)

def test_betting(gambler_id):
    print("\nBETTING\n")

    for i in range(5):
        result, balance = BettingService.place_bet(gambler_id, 100)
        print(f"Bet {i + 1}: {result}, Balance: {balance}")

def test_session_flow():
    gambler = testGambler()
    session = SessionService.start_session(gambler.gambler_id)
    print("Session started")
    SessionService.play_session(session, 100)


if __name__ == "__main__":
    test_connection()
    test_session_flow()