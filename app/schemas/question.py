from pydantic import BaseModel

from typing import List

from app.schemas.user import UserOut

class QuestionIn(BaseModel):
    question: str

class QuestionOut(BaseModel):
    id: int
    question: str
    user_id: int
    user: UserOut

    class Config:
        orm_mode = True

class QuestionListOut(BaseModel):
    questions: List[QuestionOut]