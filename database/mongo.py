# database/mongo.py
from pymongo import MongoClient
from dto.config import MDB_CONNECTION, MDB_BASE, MDB_COLLECTION

class MongoConnection:
    client: MongoClient = None
    db = None
    collection = None

    @classmethod
    def connect(cls):
        if cls.client is None:
            cls.client = MongoClient(MDB_CONNECTION)
            cls.db = cls.client[MDB_BASE]
            cls.collection = cls.db[MDB_COLLECTION]
        return cls.collection

    @classmethod
    def disconnect(cls):
        if cls.client:
            cls.client.close()
            cls.client = None
            cls.db = None
            cls.collection = None
