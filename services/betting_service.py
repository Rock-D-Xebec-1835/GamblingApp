from repositories.gambler_repository import GamblerRepository
from repositories.stake_transaction_repository import StakeTransactionRepository
from repositories.bet_repository import BetRepository
from models.transaction_type import TransactionType
from models.stake_transaction import StakeTransaction
from models.bet import Bet

import random

class BettingService:
    @staticmethod
    def place_bet(gambler_id, amount, session_id=None):
        gambler = GamblerRepository.find_by_id(gambler_id)

        if amount > gambler.current_balance:
            raise ValueError("Insufficient Balance")
        
        win = random.choice([True, False])

        if win:
            gambler.current_balance += amount
            gambler.total_winnings += amount
            result="WIN"
            txn_type = TransactionType.BET_WIN.value
        else:
            gambler.current_balance -= amount
            gambler.total_winnings -= amount
            result="LOSS"
            txn_type = TransactionType.BET_LOSS.value

        gambler.total_bets += 1
        if gambler.current_balance < gambler.min_balance:
            gambler.min_balance = gambler.current_balance
        bet = BetRepository.create(
            Bet(
                gambler_id=gambler_id,
                amount=amount,
                result=result,
                session_id=session_id
            )
        )

        StakeTransactionRepository.create(
            StakeTransaction(
                gambler_id=gambler_id,
                session_id=session_id,
                type=txn_type,
                amount=amount,
                balance_after=gambler.current_balance
            )
        )

        GamblerRepository.update(gambler)

        return result, gambler.current_balance


        