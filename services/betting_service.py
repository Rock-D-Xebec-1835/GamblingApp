from repositories.gambler_repository import GamblerRepository
from repositories.stake_transaction_repository import StakeTransactionRepository
from repositories.bet_repository import BetRepository
from models.transaction_type import TransactionType
from models.stake_transaction import StakeTransaction
from models.bet import Bet
from strategies.outcome_strategy import RandomOutcomeStrategy, WeightedProbabilityStrategy
from models.odds_config import OddsConfig
from models.game_result import GameResult
from services.input_validator import InputValidator

import random

class BettingService:
    @staticmethod
    def american_to_decimal(odds):
        if odds > 0:
            return(odds / 100) + 1
        else:
            return(100 / abs(odds)) + 1

    @staticmethod
    def place_bet(gambler_id, amount, session_id=None, win_probability=None, odds_type="PROBABILITY", outcome_strategy=None):
        gambler = GamblerRepository.find_by_id(gambler_id)

        InputValidator.validate_bet_amount(amount, gambler.current_balance)
        if(win_probability == None):
            win_probability = random.uniform(0.3,0.7)
        InputValidator.validate_probability(win_probability)

        if outcome_strategy is None:
            outcome_strategy = RandomOutcomeStrategy(win_probability)
        win = outcome_strategy.is_win()

        odds_config = OddsConfig(odds_type)
        odds = odds_config.calculate_odds(win_probability)
        stake_before = gambler.current_balance
        if win:
            decimal_odds = odds
            if(odds_config.odds_type == "AMERICAN"):
                decimal_odds = BettingService.american_to_decimal(odds)
            payout = round(amount * decimal_odds, 2)
            gambler.current_balance += round(payout - amount,2)
            gambler.total_winnings += round(payout - amount,2)
            result="WIN"
            txn_type = TransactionType.BET_WIN.value
            txn_amount = payout - amount
        else:
            gambler.current_balance -= amount
            gambler.total_winnings -= amount
            result="LOSS"
            txn_type = TransactionType.BET_LOSS.value
            txn_amount = -amount
        
        stake_after = gambler.current_balance

        gambler.total_bets += 1
        if gambler.current_balance < gambler.min_balance:
            gambler.min_balance = gambler.current_balance
        bet = BetRepository.create(
            Bet(
                gambler_id=gambler_id,
                amount=amount,
                result=result,
                session_id=session_id,
                stake_before=stake_before,
                stake_after=stake_after,
                odds=odds
            )
        )

        StakeTransactionRepository.create(
            StakeTransaction(
                gambler_id=gambler_id,
                session_id=session_id,
                type=txn_type,
                amount=txn_amount,
                balance_after=gambler.current_balance
            )
        )

        GamblerRepository.update(gambler)

        return GameResult(result, amount, odds, txn_amount, gambler.current_balance)


        