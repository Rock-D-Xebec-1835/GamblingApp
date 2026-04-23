from db.db_manager import DBManager
from models.stake_transaction import StakeTransaction

class StakeTransactionRepository:
    @staticmethod
    def create(txn: StakeTransaction):
        query = """
        INSERT INTO stake_transaction(
            gambler_id, session_id, type, amount, balance_after
        )
        VALUES(%s, %s, %s, %s, %s)
        """

        cursor = DBManager.execute_write(query, (
            txn.gambler_id,
            txn.session_id,
            txn.type,
            txn.amount,
            txn.balance_after
        ))

        txn.txn_id = cursor.lastrowid
        return txn
    
    @staticmethod
    def find_by_gambler_id(gambler_id):
        query = "SELECT * FROM stake_transaction WHERE gambler_id = %s"
        return DBManager.fetch_all(query, (gambler_id,))
    
    @staticmethod
    def find_by_session(session_id):
        query = "SELECT * FROM stake_transaction WHERE session_id = %s"
        return DBManager.fetch_all(query, (session_id,))