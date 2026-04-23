from db.db_manager import DBManager
from models.session import Session

class SessionRepository:
    @staticmethod
    def create(session: Session):
        query = """
        INSERT INTO session(gambler_id, status)
        VALUES(%s, %s)
        """

        cursor = DBManager.execute_write(query, (
            session.gambler_id,
            session.status
        ))

        session.session_id = cursor.lastrowid
        return session
    
    @staticmethod
    def end_session(session_id, reason):
        query = """
        UPDATE session
        SET status='ENDED', end_reason=%s, end_time=NOW()
        WHERE session_id=%s
        """
        DBManager.execute_write(query, (reason, session_id))

    @staticmethod
    def find_active_by_gambler(gambler_id):
        query = """
        SELECT *
        FROM session
        WHERE gambler_id = %s
        AND status = 'ACTIVE'
        LIMIT 1 
        """
        DBManager.fetch_one(query, (gambler_id,))