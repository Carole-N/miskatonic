from pymongo import MongoClient
from dto.config import MDB_CONNECTION, MDB_BASE, MDB_COLLECTION, MDB_COLLECTION2

class MongoConnection:
    client: MongoClient = None
    db = None
    collection = None
    collection2 = None
    @classmethod
    def connect(cls):
        if cls.client is None:
            cls.client = MongoClient(MDB_CONNECTION)
            cls.db = cls.client[MDB_BASE]
        if cls.collection is None:
            cls.collection = cls.db[MDB_COLLECTION]
        return cls.collection
    
    @classmethod
    def connect_coll2(cls):
        if cls.client is None:
            cls.client = MongoClient(MDB_CONNECTION)
            cls.db = cls.client[MDB_BASE]
        if cls.collection2 is None:
            cls.collection2 = cls.db[MDB_COLLECTION2]
        return cls.collection2

    @classmethod
    def disconnect(cls):
        if cls.client:
            cls.client.close()
            cls.client = None
            cls.db = None
            cls.collection = None
            cls.collection2 = None
