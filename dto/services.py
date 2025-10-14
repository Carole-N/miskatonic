# dto/services.py
from bson import ObjectId
from database.mongo import MongoConnection
from models.user_db import UserDB
from models.questions import QuestionModel
from models.user_dto import UserModel


# ---- Service MongoDB (Questions) ----
class QuestionService:
    @staticmethod
    def get_collection():
        return MongoConnection.connect()

    @classmethod
    def add_question(cls, question: QuestionModel):
        result = cls.get_collection().insert_one(question.model_dump())
        return str(result.inserted_id)

    @classmethod
    def get_all_questions(cls):
        questions = list(cls.get_collection().find())
        print("Questions récupérées dans le service:", questions)
        for q in questions:
            q["_id"] = str(q["_id"])
        return questions

    @classmethod
    def get_question_by_id(cls, question_id: str):
        q = cls.get_collection().find_one({"_id": ObjectId(question_id)})
        if q:
            q["_id"] = str(q["_id"])
        return q

    @classmethod
    def get_quizz_by_id(cls, quizz_id: str):
        q = cls.get_collection().find_one({"_id": ObjectId(quizz_id)})
        if q:
            q["_id"] = str(q["_id"])
        return q

    @classmethod
    def update_question_by_id(cls, question_id: str, update_data: dict):
        result = cls.get_collection().update_one(
            {"_id": ObjectId(question_id)}, {"$set": update_data}
        )
        return result.modified_count

    @classmethod
    def delete_question_by_id(cls, question_id: str):
        result = cls.get_collection().delete_one({"_id": ObjectId(question_id)})
        return result.deleted_count

    @classmethod
    def save_quizz_result(cls, user: str, subject: str, questions: list):
        collection = cls.get_collection_quizz()

        quizz_doc = {
            "user": user,
            "subject": subject,
            "questions": [
                {
                    "question_id": str(q.get("_id", q.get("id"))),
                    "question_text": {
                        "question": q.get("question"),
                        "responses": q.get("responses", []),
                        "good_answers_texte": q.get("good_answers_texte", []),
                        "remark": q.get("remark"),
                        "subject": q.get("subject"),
                    },
                    "selected": q.get("selected", []),
                    "correct_answers": q.get("good_answers_texte", []),
                }
                for q in questions
            ],
        }

        print("DEBUG insertion quiz:", quizz_doc)  # Pour vérifier dans la console
        collection.insert_one(quizz_doc)


# ---- Service SQLite (Utilisateurs) ----
class UserService:
    @staticmethod
    def get_all_users(db):
        return db.query(UserDB).all()

    @staticmethod
    def get_user_by_id(db, user_id: int):
        return db.query(UserDB).filter(UserDB.user_id == user_id).first()

    @staticmethod
    def add_user(db, user: UserModel):
        db_user = UserDB(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(db, user_id: int, update_data: dict):
        user = db.query(UserDB).filter(UserDB.user_id == user_id).first()
        if not user:
            return None
        for k, v in update_data.items():
            setattr(user, k, v)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db, user_id: int):
        user = db.query(UserDB).filter(UserDB.user_id == user_id).first()
        if not user:
            return None
        db.delete(user)
        db.commit()
        return user


class QuizzService:
    @classmethod
    def get_collection_quizz(cls):
        return MongoConnection.connect_coll2()

    @classmethod
    def get_all_quizzs(cls):
        quizz = list(cls.get_collection_quizz().find())
        print("Quizzs récupérées dans le service:", quizz)
        for q in quizz:
            q["_id"] = str(q["_id"])
        return quizz

    @classmethod
    def get_quizz_by_id(cls, quizz_id: str):
        q = cls.get_collection_quizz().find_one({"_id": ObjectId(quizz_id)})
        if q:
            q["_id"] = str(q["_id"])
        return q

    @classmethod
    def get_subjects_from_mongo(cls):
        questions = QuestionService.get_all_questions()
        subjects = sorted(
            set(q.get("subject", "").strip() for q in questions if q.get("subject"))
        )
        return subjects

    @classmethod
    def save_quizz_result(cls, user: str, subject: str, questions: list):
        collection = cls.get_collection_quizz()
        quizz_doc = {
            "user": user,
            "subject": subject,
            "questions": [
                {
                    "question_id": str(q.get("_id", q.get("id"))),
                    "question_text": {
                        "question": q.get("question"),
                        "responses": q.get("responses", []),
                        "good_answers_texte": q.get("good_answers_texte", []),
                        "remark": q.get("remark"),
                        "subject": q.get("subject"),
                    },
                    "selected": q.get("selected", []),
                    "correct_answers": q.get("good_answers_texte", []),
                }
                for q in questions
            ]
        }
        print("DEBUG insertion quiz:", quizz_doc)
        collection.insert_one(quizz_doc)
        
    @classmethod
    def delete_quizz_by_id(cls, quizz_id: str):
        result = cls.get_collection_quizz().delete_one({"_id": ObjectId(quizz_id)})
        return result.deleted_count
