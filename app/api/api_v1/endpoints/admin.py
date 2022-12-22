from datetime import timedelta
from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.core import security
from app.core.config import settings

from app.models.user import User

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


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


# @router.post("/register", response_model=schemas.UserOut, status_code = 201)
# def register( form_data: schemas.Register, db: Session = Depends(deps.get_db) ) -> Any:
#     """
#     Create a new user.
#     Arguments:
#     form_data: user_type, first_name, last_name, email, password, confirm_password, unique_id
#     db: yields database session
#     Returns:
#     new user or error
#     """

#     if form_data.password != form_data.confirm_password:
#         raise HTTPException(
#             status_code=400,
#             detail="Password does not match.",
#         )

#     user = crud.user.get_by_email(db, email=form_data.email)
    
#     if user:
#         raise HTTPException(
#             status_code=400,
#             detail="This email is already in use. Kindly contact the administrator.",
#         )

#     user = crud.user.get_by_roll_number(db, roll_number = form_data.roll_no)

#     if user:
#         if form_data.user_type == 0:
#             raise HTTPException(
#             status_code=400,
#             detail="This roll number is already in use. Kindly contact the administrator.",
#         )
#         elif form_data.user_type == 1:
#             raise HTTPException(
#             status_code=400,
#             detail="This faculty number is already in use. Kindly contact the administrator.",
#         )
#         elif form_data.user_type == 2:
#             raise HTTPException(
#             status_code=400,
#             detail="This roll number is already in use. Kindly contact the administrator.",
#         )
    
#     user = crud.user.create(db, obj_in=form_data)
    
#     return user


@router.get("/inactive_users", response_model=schemas.UserListOut)
def get_all_inactive_users(db: Session = Depends(deps.get_db)) -> List[User]:
    """
    Returns all inactive users from the database.
    Arguments:
    db: yields database session
    Returns:
    all users or []
    """

    inactive_users = crud.user.get_all_inactive_users(db)

    return {
        "users": inactive_users,
    }

def send_email(email: str, message=""):
    message = Mail(
        from_email='vaibhav.vk2128@gmail.com',
        to_emails=email,
        subject='Regarding account approval in Univcomm app',
        html_content=message)
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

@router.patch('/activate_user/{user_id}', response_model = schemas.UserOut)
def activate_user(user_id: int, background_tasks: BackgroundTasks, db: Session = Depends(deps.get_db)) -> Any:
    user = crud.user.get_by_user_id(db, user_id = user_id)

    updated_user = crud.user.update_user(db, user)

    message = f'<strong>Congratulations {updated_user.first_name}! Your account has been verified. Now you can login to the app and start interacting.</strong>'

    background_tasks.add_task(send_email, email = f'{updated_user.email}', message=message)

    return user