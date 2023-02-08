import psycopg2
from psycopg2._psycopg import cursor, connection

from abstract.abstract_settings import AbstractSettings
from abstract.db_connection_operations import DBConnectionOperations
from abstract.settings_provider import SettingsProvider


class DBConnection(DBConnectionOperations):
    def __init__(self, settings_provider: SettingsProvider):
        self.settings_provider = settings_provider
        self.settings = self.settings_provider.get_settings()

    @staticmethod
    def begin_exec(settings: AbstractSettings) -> connection:
        return psycopg2.connect(
            host=settings.get('db_host'),
            port=settings.get('db_port'),
            database=settings.get('db_name'),
            user=settings.get('db_user'),
            password=settings.get('db_password')
        )

    @staticmethod
    def end_exec(conn):
        if conn is not None:
            conn.close()

    def exec(self, sql: str):
        try:
            conn = DBConnection.begin_exec(self.settings)
            cur: cursor = conn.cursor()
            cur.execute(sql)
            conn.commit()
        finally:
            DBConnection.end_exec(conn)

    def fetch_one(self, sql: str):
        try:
            conn = DBConnection.begin_exec(self.settings)
            cur: cursor = conn.cursor()
            cur.execute(sql)
            return cur.fetchone()
        finally:
            DBConnection.end_exec(conn)

    def fetch_all(self, sql: str):
        try:
            conn = DBConnection.begin_exec(self.settings)
            cur: cursor = conn.cursor()
            cur.execute(sql)
            return cur.fetchall()
        finally:
            DBConnection.end_exec(conn)
