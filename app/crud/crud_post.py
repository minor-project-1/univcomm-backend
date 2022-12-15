from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from app.models.user import Post

from app.crud.base import CRUDBase

from app.schemas.post import PostIn

class CRUDPost(CRUDBase):
    def get_all(self, db: Session, user_id: int)-> List[Post]:
        return db.query(Post).filter(Post.user_id != user_id).all()

    def create(self, db: Session, *, obj_in: PostIn, user_id: int) -> Post:

        db_obj = Post(
            title = obj_in.title,
            content = obj_in.content,
            user_id = user_id
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj


post = CRUDPost(Post)