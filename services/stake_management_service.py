from repositories.gambler_repository import GamblerRepository
from repositories.stake_transaction_repository import StakeTransactionRepository
from models.stake_transaction import StakeTransaction
from models.transaction_type import TransactionType

class StakeManagementService:
    @staticmethod
    def deposit(gambler_id, amount):
        gambler = GamblerRepository.find_by_id(gambler_id)

        gambler.current_balance += amount

        StakeTransactionRepository.create(
            StakeTransaction(
                gambler_id=gambler_id,
                type=TransactionType.DEPOSIT.value,
                amount=amount,
                balance_after=gambler.current_balance
            )
        )

        GamblerRepository.update(gambler)
        return gambler

    @staticmethod
    def withdraw(gambler_id, amount):
        gambler = GamblerRepository.find_by_id(gambler_id)

        if gambler.current_balance < amount:
            raise ValueError("Insufficient Balance")
        
        gambler.current_balance -= amount

        StakeTransactionRepository.create(
            StakeTransaction(
                gambler_id=gambler_id,
                type=TransactionType.WITHDRAWAL.value,
                amount=amount,
                balance_after=gambler.current_balance
            )
        )

        GamblerRepository.update(gambler)
        return gambler
    
    @staticmethod
    def get_transaction_history(gambler_id):
        return StakeTransactionRepository.find_by_gambler_id(gambler_id)
    
    @staticmethod
    def get_session_transactions(session_id):
        return StakeTransactionRepository.find_by_session(session_id)
    
    @staticmethod
    def print_transactions(txns):
        print("\nTRANSACTIONS")
        for t in txns:
            print(t)
