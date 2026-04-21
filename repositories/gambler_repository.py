from db.db_manager import DBManager
from models.gambler import Gambler

class GamblerRepository:
    @staticmethod
    def create(gambler: Gambler):
        query = """
        INSERT INTO gambler (name, initial_balance, current_balance, total_winnings, total_bets, min_balance, win_threshold, loss_threshold)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor = DBManager.execute_write(query, (
            gambler.name,
            gambler.initial_balance,
            gambler.current_balance,
            gambler.total_winnings,
            gambler.total_bets,
            gambler.min_balance,
            gambler.win_threshold,
            gambler.loss_threshold,
        ))
        gambler.gambler_id = cursor.lastrowid
        return gambler
    
    @staticmethod
    def find_by_id(gambler_id: int):
        query = "SELECT * FROM gambler WHERE gambler_id = %s"
        result = DBManager.fetch_one(query, (gambler_id,))
        if not result:
            return None
        return Gambler(**result)
    
    @staticmethod
    def update(gambler: Gambler):
        query = """
        UPDATE gambler
        SET name=%s, current_balance=%s, total_winnings=%s, total_bets=%s, min_balance=%s, win_threshold=%s, loss_threshold=%s
        WHERE gambler_id=%s
        """

        DBManager.execute_write(query, (
            gambler.name,
            gambler.current_balance,
            gambler.total_winnings,
            gambler.total_bets,
            gambler.min_balance,
            gambler.win_threshold,
            gambler.loss_threshold,
            gambler.gambler_id
        ))
