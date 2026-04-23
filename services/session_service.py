from repositories.session_repository import SessionRepository
from models.session import Session
from repositories.gambler_repository import GamblerRepository
from services.betting_service import BettingService
from models.stake_boundary import StakeBoundary
from models.session_statistics import SessionStatistics
from services.stake_management_service import StakeManagementService
from strategies import base_strategy, fixed_strategy, martingale_strategy, percentage_strategy
from models.session_parameters import SessionParameters
import time
import random
from models.pause_record import PauseRecord



class SessionService:
    @staticmethod
    def start_session(gambler_id):
        gambler = GamblerRepository.find_by_id(gambler_id)
        existing = SessionRepository.find_active_by_gambler(gambler_id)
        if existing:
            raise Exception("Active session alread exists for the user")
        # RESET STATE FOR NEW SESSION
        gambler.current_balance = gambler.initial_balance
        gambler.min_balance = gambler.initial_balance
        GamblerRepository.update(gambler)
        return SessionRepository.create(
            Session(
                gambler_id=gambler_id
            )
        )
    
    def pause_session(session, reason="MANUAL"):
        if session.status != "ACTIVE":
            return
        
        session.status = "PAUSED"
        session.paused_at = time.time()
        print("Session Paused")

    def resume_session(session):
        if session.status != "PAUSED":
            return
        
        pause_end = time.time()
        pause_record = PauseRecord(
            start_time=session.paused_at,
            end_time=pause_end
        )

        session.pause_records.append(pause_record)
        session.total_pause_time += pause_record.duration()
        session.paused_at = None
        session.status = "ACTIVE"
        print("Session resumed")

    @staticmethod
    def play_session(session, strategy, params: SessionParameters):
        session.status = "ACTIVE"
        gambler = GamblerRepository.find_by_id(session.gambler_id)
        boundary = StakeBoundary(
            params.win_threshold,
            params.loss_threshold
        )

        stats = SessionStatistics()

        print(f"\nSTRATEGY: {strategy.__class__.__name__}")

        start_time = time.time()
        games_played = 0

        while session.status != "ENDED":
            if session.status == "PAUSED":
                time.sleep(1)
                continue
            elapsed_time = (time.time() - start_time) - session.total_pause_time

            if games_played == 3:
                SessionService.pause_session(session)
                time.sleep(3)
                SessionService.resume_session(session)

            if games_played >= params.max_games:
                SessionRepository.end_session(session.session_id, "MAX_GAMES")
                session.status = "ENDED"
                session.end_reason = "MAX_GAMES"
                print("Session Ended: MAX_GAMES reached")
                break
            if elapsed_time >= params.max_duration:
                SessionRepository.end_session(session.session_id, "TIMEOUT")
                session.status = "ENDED"
                session.end_reason = "TIMEOUT"
                print("Session Ended: TIMEOUT reached")
                break

            amount = strategy.next_bet(gambler)
            amount = max(params.min_bet, min(amount, params.max_bet))
            amount = min(amount, gambler.current_balance)
            win_probability = (
                params.win_probability
                if params.win_probability is not None
                else random.uniform(0.3, 0.7)
            )
            # PLACE BET
            result, balance = BettingService.place_bet(
                gambler.gambler_id,
                amount,
                session.session_id,
                win_probability=win_probability
            )

            games_played += 1

            # UPDATE STRATEGY
            strategy.record_result(result)

            # UPDATE STATS
            stats.record(result, amount)

            print(f"Bet: {amount} | Result: {result}, Balance: {balance}")

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
        print(f"Games Played: {games_played}")
        print(f"Total Duration: {round(time.time() - start_time, 2)} sec")
        print(f"Total Pause Duration: {round(session.total_pause_time,2)}")
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