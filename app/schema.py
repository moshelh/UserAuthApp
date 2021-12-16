from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

    class Config:
        orm_mode = True


class UserInDB(User):
    password: str

    class Config:
        orm_mode = True


class UserLogIn(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
