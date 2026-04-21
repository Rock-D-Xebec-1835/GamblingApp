# db/db_manager.py

from db.connection import DatabaseConnection

class DBManager:

    @staticmethod
    def execute_write(query, params=None):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return cursor

    @staticmethod
    def fetch_one(query, params=None):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = cursor.fetchone()
        cursor.close()
        return result

    @staticmethod
    def fetch_all(query, params=None):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        cursor.close()
        return result
    
    