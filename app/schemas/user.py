from pydantic import BaseModel

from typing import List


class UserOut(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    roll_no: str
    user_type: int
    is_active: int

    class Config:
        orm_mode = True

class UserIn(BaseModel):
    user_type: int
    first_name: str
    last_name: str
    email: str
    password: str
    roll_no: str

class UserListOut(BaseModel):
    users: List[UserOut]