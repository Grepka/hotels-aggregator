from fastapi import APIRouter
from passlib.context import CryptContext

from src.database import async_session_maker
from src.schemas.user import UserRequestAdd, UserAdd
from src.repositories.user import UserRepositories


router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация пользователей"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def create_user(user_data: UserRequestAdd):
    hashed_password = pwd_context.hash(user_data.password)
    new_user_data = UserAdd(email=user_data.email, password=hashed_password)
    async with async_session_maker() as session:
        await UserRepositories(session).add(new_user_data)
        await session.commit()
        return {"result": "OK"}
