from db.db_manager import DBManager
from services.gambler_service import GamblerService
from repositories.gambler_repository import GamblerRepository
from services.stake_management_service import StakeManagementService
from services.betting_service import BettingService
from services.session_service import SessionService
from strategies import FixedAmountStrategy, PercentageStrategy, MartingaleStrategy, FibonacciStrategy
from models.session_parameters import SessionParameters
from strategies.outcome_strategy import RandomOutcomeStrategy, WeightedProbabilityStrategy
from models.odds_config import OddsConfig
import random
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
def reset_gambler(gambler_id):
    gambler = GamblerRepository.find_by_id(gambler_id)
    gambler.current_balance = gambler.initial_balance
    gambler.min_balance = gambler.initial_balance
    gambler.total_winnings = 0
    gambler.total_bets = 0
    GamblerRepository.update(gambler)
# TEST STAKE
def testStake(gambler_id):
    print("\nDEPOSIT\n")
    g = StakeManagementService.deposit(gambler_id, 500)
    print("Balance after deposit: ", g.current_balance)
    print("\nWITHDRAWAL\n")
    g = StakeManagementService.withdraw(gambler_id, 500)
    print("Balance after withdrawal: ", g.current_balance)

def test_betting(gambler_id):
    gambler = GamblerRepository.find_by_id(gambler_id)

    for _ in range(5):
        if gambler.current_balance <= 0:
            print("Balance exhausted, stopping test")
            break

        amount = min(100, gambler.current_balance)

        result, balance = BettingService.place_bet(
            gambler_id,
            amount,
            session_id=None,
            win_probability=random.uniform(0.3, 0.7)
        )

        print(f"Result: {result}, Balance: {balance}")

        gambler.current_balance = balance

params = SessionParameters(
    win_threshold=2000,
    loss_threshold=500,
    min_bet=50,
    max_bet=500,
    # max_games=10,
    max_duration=30,
    win_probability=None
)

def test_session_flow():
    gambler = testGambler()
    session = SessionService.start_session(gambler.gambler_id)
    print("Session started")
    strategy = FixedAmountStrategy(100)
    SessionService.play_session(session, strategy, params=params)

def test_outcomes():
    print("\n--- Testing Outcome Strategies ---")

    random_strategy = RandomOutcomeStrategy(0.5)
    weighted_strategy = WeightedProbabilityStrategy(0.5, house_edge=0.1)

    random_wins = 0
    weighted_wins = 0

    for _ in range(1000):
        if random_strategy.is_win():
            random_wins += 1
        if weighted_strategy.is_win():
            weighted_wins += 1

    print(f"Random Win Rate: {random_wins / 1000}")
    print(f"Weighted Win Rate: {weighted_wins / 1000}")

def test_odds():
    print("\n--- Testing Odds Systems ---")

    prob = 0.4

    for odds_type in ["FIXED", "PROBABILITY", "DECIMAL", "AMERICAN"]:
        config = OddsConfig(odds_type)
        odds = config.calculate_odds(prob)
        print(f"{odds_type}: {odds}")

result = BettingService.place_bet(
    gambler_id=1,
    amount=100,
    win_probability=0.5,
    odds_type="AMERICAN",
    outcome_strategy=WeightedProbabilityStrategy(0.5, 0.05)
)



if __name__ == "__main__":
    test_connection()
    test_session_flow()
    # test_outcomes()
    # test_odds()
    # gambler = testGambler()
    # reset_gambler(gambler.gambler_id)
    # test_betting(gambler.gambler_id)
    # print(result)
