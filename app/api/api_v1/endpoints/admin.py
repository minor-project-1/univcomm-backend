from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.core import security
from app.core.config import settings

router = APIRouter()


@router.post("/auth/login", response_model=schemas.Token)
def login(form_data: schemas.Login, db: Session = Depends(deps.get_db) ) -> Any:
    """
    Log in the admin using email and password.
    Arguments:
    form_data: email and password
    db: yields database session
    Returns:
    access_token or error
    """

    admin = crud.admin.authenticate(
        db, email=form_data.email, password=form_data.password
    )

    if not admin:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    return {
        "access_token": security.create_access_token(
            admin.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/register", response_model=schemas.UserOut, status_code = 201)
def register( form_data: schemas.Register, db: Session = Depends(deps.get_db) ) -> Any:
    """
    Create a new user.
    Arguments:
    form_data: user_type, first_name, last_name, email, password, confirm_password, unique_id
    db: yields database session
    Returns:
    new user or error
    """

    if form_data.password != form_data.confirm_password:
        raise HTTPException(
            status_code=400,
            detail="Password does not match.",
        )

    user = crud.user.get_by_email(db, email=form_data.email)
    
    if user:
        raise HTTPException(
            status_code=400,
            detail="This email is already in use. Kindly contact the administrator.",
        )

    user = crud.user.get_by_roll_number(db, roll_number = form_data.roll_no)

    if user:
        if form_data.user_type == 0:
            raise HTTPException(
            status_code=400,
            detail="This roll number is already in use. Kindly contact the administrator.",
        )
        elif form_data.user_type == 1:
            raise HTTPException(
            status_code=400,
            detail="This faculty number is already in use. Kindly contact the administrator.",
        )
        elif form_data.user_type == 2:
            raise HTTPException(
            status_code=400,
            detail="This roll number is already in use. Kindly contact the administrator.",
        )
    
    user = crud.user.create(db, obj_in=form_data)
    
    return user