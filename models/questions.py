from pydantic import BaseModel


class QuestionModel(BaseModel):
    question: str
    subject: str
    use: str
    correct: list[str]
    responses: list[str]
    good_answer_texte: list[str]
    remark: str | None
