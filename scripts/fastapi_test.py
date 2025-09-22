from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import json
import os

app = FastAPI()

class Question(BaseModel):
    id: int
    question: str
    subject: str
    use: str
    correct: Optional[str]
    responses: List
    good_answers_texte: List[str]
    remark: Optional[str] = None  # nullable

@app.get("/questions", response_model=List[Question])
def get_questions():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "..", "data", "questions.json")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
