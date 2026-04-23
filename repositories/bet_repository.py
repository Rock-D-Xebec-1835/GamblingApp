from db.db_manager import DBManager
from models.bet import Bet

class BetRepository:
    @staticmethod
    def create(bet: Bet):
        query = """
        INSERT INTO bet(gambler_id, session_id, amount, result)
        VALUES(%s, %s, %s, %s)
        """
        cursor = DBManager.execute_write(query, (
            bet.gambler_id,
            bet.session_id,
            bet.amount,
            bet.result
        ))

        bet.bet_id = cursor.lastrowid
        return bet
    