from pydantic import BaseModel

from typing import List

from app.schemas.user import UserOut

class PostIn(BaseModel):
    title: str
    content: str

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    user: UserOut

    class Config:
        orm_mode = True

class PostListOut(BaseModel):
    posts: List[PostOut]