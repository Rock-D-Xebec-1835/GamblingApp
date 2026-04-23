from repositories.gambler_repository import GamblerRepository
from repositories.stake_transaction_repository import StakeTransactionRepository
from repositories.bet_repository import BetRepository
from models.transaction_type import TransactionType
from models.stake_transaction import StakeTransaction
from models.bet import Bet

import random

class BettingService:
    @staticmethod
    def place_bet(gambler_id, amount, session_id=None, win_probability=None):
        gambler = GamblerRepository.find_by_id(gambler_id)

        if amount > gambler.current_balance:
            raise ValueError("Insufficient Balance")
        if(win_probability == None):
            win_probability = random.uniform(0.3,0.7)
        if(win_probability <= 0 or win_probability >= 1):
            raise ValueError("Win probability must be between 0 and 1")

        win = random.random() < win_probability

        odds = round(1 / win_probability,2)
        stake_before = gambler.current_balance
        if win:
            payout = round(amount * odds, 2)
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

        return result, gambler.current_balance


        