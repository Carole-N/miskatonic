from dto.connexion import Connexion
from models.questions import QuestionModel
from bson import ObjectId


class QuestionService:
    @classmethod
    def get_collection(cls):
        return Connexion.get_db()["question"]

    @classmethod
    def add_question(cls, question: QuestionModel):
        result = cls.get_collection().insert_one(question.model_dump())
        return str(result.inserted_id)

    @classmethod
    def get_question_by_id(cls, question_id: str):
        question = list(cls.get_collection().find_one({"_id": ObjectId(question_id)}))
        if question:
            question["_id"] = str(question["_id"])
        return question

    @classmethod
    def get_all_questions(cls):
        questions = list(cls.get_collection().find())
        for q in questions:
            q["_id"] = str(q["_id"])
        return questions

    @classmethod
    def update_question_by_id(cls, question_id: str, update_data: dict):
        result = cls.get_collection().update_one(
            {"_id": ObjectId(question_id)}, {"$set": update_data}
        )
        return result.modified_count  # 0 if nothing updated

    @classmethod
    def delete_question_by_id(cls, question_id: str):
        result = cls.get_collection().delete_one({"_id": ObjectId(question_id)})
        return result.deleted_count  # 0 if nothing deleted
