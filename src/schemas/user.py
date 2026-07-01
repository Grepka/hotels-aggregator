from pydantic import BaseModel


class UserRequestAdd(BaseModel):
    email: str
    password: str

class UserAdd(BaseModel):
    email: str
    # Переименовать хешированный при следующей миграции
    password: str

class User(BaseModel):
    id: int
    email: str

