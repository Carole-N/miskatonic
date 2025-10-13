# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from dto.services import QuestionService, UserService, QuizzService
from database.sqlite import get_db_sqlite
from models.questions import QuestionModel
from models.user_dto import UserModel

app = FastAPI(title="Quiz API")


@app.get("/")
def root():
    return {"message": "API running"}


# --- Questions (MongoDB) ---
@app.post("/question", tags=["Questions"])
def add_question(question: QuestionModel):
    return {"id": QuestionService.add_question(question)}


@app.get("/question", tags=["Questions"])
def get_all_questions():
    questions = QuestionService.get_all_questions()
    print("Raw questions:", questions)
    return questions


@app.get("/question/{question_id}", tags=["Questions"])
def get_question_by_id(question_id: str):
    q = QuestionService.get_question_by_id(question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return q


@app.put("/question/{question_id}", tags=["Questions"])
def update_question_by_id(
    question_id: str,
    question: str,
    subject: str,
    use: str,
    correct: list[str],
    responses: list[str],
    good_answer_texte: list[str],
    remark: str | None,
):
    update_data = {
        "question:": question,
        "subject": subject,
        "use": use,
        "correct": correct,
        "responses": responses,
        "good_answer_texte": good_answer_texte,
        "reamark": remark,
    }
    modified_count = QuestionService.update_question_by_id(question_id, update_data)
    if modified_count == 0:
        return {"error": "Question not found"}
    return {"message": "Question successfully modified"}


@app.delete("/question/{question_id}", tags=["Questions"])
def delete_question_by_id(question_id: str):
    deleted_count = QuestionService.delete_question_by_id(question_id)
    if deleted_count == 0:
        return {"error": "Question not found"}
    return {"message": "Question deleted successfully"}


# --- Utilisateurs (SQLite) ---
@app.get("/users", response_model=list[UserModel], tags=["Users"])
def get_users(db: Session = Depends(get_db_sqlite)):
    users = UserService.get_all_users(db)
    return [UserModel.model_validate(u) for u in users]


@app.post("/users", tags=["Users"])
def add_user(user: UserModel, db: Session = Depends(get_db_sqlite)):
    # Vérifier si le nom d'utilisateur existe déjà
    all_users = UserService.get_all_users(db)
    if any(u.user_name == user.user_name for u in all_users):
        raise HTTPException(status_code=400, detail="User already exists")

    # Forcer role_id à 3 (élève)
    user.role_id = 3

    return UserService.add_user(db, user)


@app.post("/login", tags=["Users"])
def login_user(user: UserModel, db: Session = Depends(get_db_sqlite)):
    all_users = UserService.get_all_users(db)
    db_user = next((u for u in all_users if u.user_name == user.user_name), None)
    if not db_user or db_user.password_hash != user.password_hash:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}


# --- Quizz (MongoDB) ---

app.get("/quizz/{quizz_id}", tags=["Quizz"])
def get_quizz_by_id():
    quizz = QuizzService.get_quizz_by_id()
    if not quizz:
        raise HTTPException(status_code=404, detail="Quizz not found")
    return quizz

@app.get("/quizz", tags=["Quizz"])
def get_all_questions():
    quizzs = QuizzService.get_all_quizzs()
    print("Raw quizz:", quizzs)
    return quizzs

@app.delete("/quizz/{quizz_id}", tags=["Quizz"])
def delete_question_by_id(question_id: str):
    deleted_count = QuestionService.delete_question_by_id(question_id)
    if deleted_count == 0:
        return {"error": "Question not found"}
    return {"message": "Question deleted successfully"}