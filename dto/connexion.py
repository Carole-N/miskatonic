from database.sqlite import get_db_sqlite
from database.mongo import MongoConnection


class Connexion:
    @staticmethod
    def get_sqlite():
        return get_db_sqlite()

    @staticmethod
    def get_mongo():
        return MongoConnection.connect()
