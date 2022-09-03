from pydantic import BaseModel


class UserOut(BaseModel):
    id: int
    email: str
    roll_no: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True

class UserIn(BaseModel):
    user_type: int
    first_name: str
    last_name: str
    email: str
    password: str
    roll_no: str