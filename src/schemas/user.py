from pydantic import BaseModel, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str


class UserAdd(BaseModel):
    email: EmailStr
    # Переименовать хешированный при следующей миграции
    password: str


class User(BaseModel):
    id: int
    email: EmailStr

class UserWithHashPassword(User):
    password: str

