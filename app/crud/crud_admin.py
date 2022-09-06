from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.admin import Admin


from app.core.security import verify_password, get_password_hash

from app.crud.base import CRUDBase

from app.schemas.auth import Register

class CRUDAdmin(CRUDBase):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Admin]:
        return db.query(Admin).filter(Admin.email == email).first()

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

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[Admin]:
        admin = self.get_by_email(db, email=email)

        if not admin:
            return None
        if not verify_password(password, admin.password):
            return None
        return admin
    

admin = CRUDAdmin(Admin)