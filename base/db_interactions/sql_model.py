import os
import configparser
import psycopg2
from psycopg2 import extras

class PgsqlCRUD:
    @staticmethod
    def get_creds():
        config = configparser.ConfigParser()
        config.read("./config/config.ini")
        return config['pg_db']


    @classmethod
    def pgsql_select(cls, request):
        db_creds = cls.get_creds()
        with psycopg2.connect(**db_creds) as connect:
            cursor = connect.cursor(cursor_factory=extras.RealDictCursor)
            if request.startswith('SELECT'):
                cursor.execute(request)
                response = cursor.fetchall()
                return response

    @classmethod
    def pgsql_delete(cls, request):
        db_creds = cls.get_creds()
        with psycopg2.connect(**db_creds) as connect:
            cursor = connect.cursor()
            if request.startswith('DELETE'):
                cursor.execute(request)
                connect.commit()
                return True
            else:
                return False

    @classmethod
    def pgsql_update(cls, request):
        db_creds = cls.get_creds()
        with psycopg2.connect(**db_creds) as connect:
            cursor = connect.cursor()
            if request.startswith('UPDATE'):
                cursor.execute(request)
                connect.commit()
                return True
            else:
                return False

    @classmethod
    def pgsql_insert(cls, request):
        db_creds = cls.get_creds()
        with psycopg2.connect(**db_creds) as connect:
            try:
                cursor = connect.cursor()
                if request.startswith('INSERT'):
                    cursor.execute(request)
                    return cursor.statusmessage
            except:
                return False