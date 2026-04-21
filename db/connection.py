# db/connection.py

import mysql.connector
from config.settings import Settings

class DatabaseConnection:
    _connection = None

    @classmethod
    def get_connection(cls):
        if cls._connection is None:
            cls._connection = mysql.connector.connect(
                host=Settings.DB_HOST,
                port=Settings.DB_PORT,
                database=Settings.DB_NAME,
                user=Settings.DB_USER,
                password=Settings.DB_PASSWORD
            )
        return cls._connection

    @classmethod
    def close_connection(cls):
        if cls._connection is not None:
            cls._connection.close()
            cls._connection = None