from pymongo import MongoClient
from dto.config import MDB_CONNECTION, MDB_BASE, MDB_COLLECTION
from bson import ObjectId

client = MongoClient(MDB_CONNECTION)

class Connexion:
    @classmethod
    def connect(cls):
        cls.client = MongoClient(MDB_CONNECTION)
        cls.db = client[MDB_BASE]
        cls.collection = cls.db[MDB_COLLECTION]
    @classmethod
    def get_all_questions(cls):
        return list(cls.collection.find())
    @classmethod
    def get_question_by_id(cls, question_id):
        return cls.collection.find_one({"_id":ObjectId(question_id)})
    @classmethod
    def add_question(cls, question_data):
        return cls.collection.insert_one(question_data).inserted_id
    @classmethod
    def update_question(cls, question_id, update_question):
        cls.collection.update_one({"_id":ObjectId(question_id)},{"$set":update_question})
    @classmethod
    def delete_question(cls, question_id):
        cls.collection.delete_one({"_id":ObjectId(question_id)})
    @classmethod
    def disconnect(cls):
        cls.client.close()
