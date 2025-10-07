from fastapi import FastAPI
from dto.connexion import Connexion
from dto.services import QuestionService
from models.questions import QuestionModel

app = FastAPI()

Connexion.connect()

@app.get("/")
def fast_root():
    return {"message": "API running"}

@app.post("/question")
def fast_add_question(question: QuestionModel):
    id_question = QuestionService.add_question(question)
    return {"id": id_question}

@app.get("/question")
def fast_get_all_questions():  
    return QuestionService.get_all_questions()

@app.get("/question")
def fast_get_question_by_id(question_id: str):
    question = QuestionService.get_question_by_id(question_id)
    if question is None:
        return {"error": "Question not found"}
    return question

@app.put("/question/{question_id}")
def fast_update_question(question_id: str, question: str, subject: str, use: str, correct: list[str], responses: list[str], good_answer_texte: str, remark: str|None):
    update_data = {"question": question, "subject": subject, "use": use, "correct": correct, "responses": responses, "good_answer_texte": good_answer_texte, "remark": remark}
    modified_count = QuestionService.update_question_by_id(question_id, update_data)
    if modified_count == 0:
        return {"error": "Question not found"}
    return {"message": "Question successfully modified"}

@app.delete("/question/{question_id}")
def fast_delete_question(question_id: str):
    deleted_count = QuestionService.delete_question_by_id(question_id)
    if deleted_count == 0:
        return {"error": "Question not found"}
    return {"message": "Question deleted successfully"}