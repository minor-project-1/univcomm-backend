from re import S
from pydantic import BaseModel


class Login(BaseModel):
    email: str
    password: str

class Register(BaseModel):
    user_type: int
    first_name: str
    last_name: str
    email: str
    password: str
    confirm_password: str
    roll_no: str