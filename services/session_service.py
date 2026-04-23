from repositories.session_repository import SessionRepository
from models.session import Session
from repositories.gambler_repository import GamblerRepository
from services.betting_service import BettingService
from models.stake_boundary import StakeBoundary
from models.session_statistics import SessionStatistics
from services.stake_management_service import StakeManagementService


class SessionService:
    @staticmethod
    def start_session(gambler_id):
        gambler = GamblerRepository.find_by_id(gambler_id)
        # RESET STATE FOR NEW SESSION
        gambler.current_balance = gambler.initial_balance
        gambler.min_balance = gambler.initial_balance
        GamblerRepository.update(gambler)
        return SessionRepository.create(
            Session(
                gambler_id=gambler_id
            )
        )
    

    @staticmethod
    def play_session(session, bet_amount):
        gambler = GamblerRepository.find_by_id(session.gambler_id)

        boundary = StakeBoundary(
            gambler.win_threshold,
            gambler.loss_threshold
        )

        stats = SessionStatistics()

        while session.status == "ACTIVE":
            # PLACE BET
            result, balance = BettingService.place_bet(
                gambler.gambler_id,
                bet_amount,
                session.session_id
            )

            # UPDATE STATS
            stats.record(result, bet_amount)

            print(f"Result: {result}, Balance: {balance}")

            # CHECK BOUNDARIES
            
            warning = boundary.check_warning(balance)
            if warning == "WIN_WARNING":
                print("Approaching WIN threshold")
            elif warning == "LOSS_WARNING":
                print("Approaching LOSS threshold")
            

            # CHECK LIMIT
            limit = boundary.check_limit(balance)

            if limit == "WIN_LIMIT":
                SessionRepository.end_session(session.session_id, "WIN_LIMIT")
                session.status = "ENDED"
                session.end_reason = "WIN_LIMIT"
                print("Session Ended: WIN_LIMIT reached")
                break
            if limit == "LOSS_LIMIT":
                SessionRepository.end_session(session.session_id, "LOSS_LIMIT")
                session.status = "ENDED"
                session.end_reason = "LOSS_LIMIT"
                print("Session Ended: LOSS_LIMIT reached")
                break

        # PRINT FINAL STATS
        SessionService.print_summary(stats)
        # txns = StakeManagementService.get_session_transactions(session.session_id)
        # StakeManagementService.print_transactions(txns)

    @staticmethod
    def print_summary(stats):
        print("\nSESSION SUMMARY\n")
        print(f"Total Bets: {stats.total_bets}")
        print(f"Wins: {stats.wins}")
        print(f"Losses: {stats.losses}")
        print(f"Win Rate: {stats.win_rate():.2f}%")
        print(f"Net Profit: {stats.net_profit}")
        print(f"Max Streak: {stats.max_streak}")