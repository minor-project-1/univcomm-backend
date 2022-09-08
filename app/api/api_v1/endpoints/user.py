from datetime import timedelta
from typing import Any, Union

from fastapi import APIRouter, Body, Depends, HTTPException, Request, Header
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.schemas import user

router = APIRouter()

@router.post("/ask", response_model= schemas.QuestionOut)
def ask(form_data: schemas.QuestionIn, db: Session = Depends(deps.get_db), token: Union[str, None] = Header(default=None) ) -> Any:
    """
    Adds a question to the database for a particular user.
    Arguments:
    db: yields database session
    Returns:
    question or error
    """

    if token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_id = security.verify_token(token)

    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    

    question = crud.question.create(db, obj_in = form_data, user_id = user_id)
    
    return question


@router.post("/post", response_model= schemas.PostOut)
def ask(form_data: schemas.PostIn, db: Session = Depends(deps.get_db), token: Union[str, None] = Header(default=None) ) -> Any:
    """
    Adds a post to the database for a particular user.
    Arguments:
    db: yields database session
    Returns:
    post or error
    """

    if token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_id = security.verify_token(token)

    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    

    post = crud.post.create(db, obj_in = form_data, user_id = user_id)
    
    return post