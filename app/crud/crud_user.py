from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from app.models.user import User, StudentData, FacultyData, AlumniData

from app.core.security import verify_password, get_password_hash

from app.crud.base import CRUDBase

from app.schemas.auth import Register

class CRUDUser(CRUDBase):
    def get_all_inactive_users(self, db: Session)-> List[User]:
        return db.query(User).filter(User.is_active == 0).all()


    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_user_id(self, db: Session, *, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()


    def get_by_roll_number(self, db: Session, *, roll_number: str) -> Optional[User]:
        return db.query(User).filter(User.roll_no == roll_number).first()

    def create(self, db: Session, *, obj_in: Register) -> User:
        db_obj = User(
            user_type  = obj_in.user_type,
            first_name = obj_in.first_name,
            last_name = obj_in.last_name,
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            roll_no = obj_in.roll_no, 
            is_active=0
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        profile = None

        if obj_in.user_type == 0:
            profile = StudentData(user_id=db_obj.id)
        elif obj_in.user_type == 1:
            profile = FacultyData(user_id=db_obj.id)
        elif obj_in.user_type == 2:
            profile = AlumniData(user_id=db_obj.id)

        db.add(profile)
        db.commit()

        return db_obj

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)

        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user
    
    def is_active(self, user: User) -> int:
        return user.is_active

    def update_user(self, db: Session, user: User) -> Optional[User]:
        user.is_active = 1

        db.add(user)
        db.commit()
        db.refresh(user)

        return user




user = CRUDUser(User)