from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from app.models.user import Question

from app.core.security import verify_password, get_password_hash

from app.crud.base import CRUDBase

from app.schemas.question import QuestionIn, QuestionOut

class CRUDQuestion(CRUDBase):
    def get_all(self, db: Session, user_id: int)-> List[Question]:
        return db.query(Question).filter(Question.user_id != user_id).all()

    def create(self, db: Session, *, obj_in: QuestionIn, user_id: int) -> Question:

        db_obj = Question(
            question = obj_in.question,
            user_id = user_id
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj


question = CRUDQuestion(Question)