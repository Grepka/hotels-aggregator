import jwt
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, Response, status
from pwdlib import PasswordHash


from src.config import settings
from src.database import async_session_maker
from src.schemas.user import UserRequestAdd, UserAdd, User
from src.repositories.user import UserRepositories


password_hash = PasswordHash.recommended()

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация пользователей"])

JWT_SECRET = settings.JWT_SECRET
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expired_in = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expired_in})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)

@router.post("/register")
async def create_user(user_data: UserRequestAdd):
    hashed_password = hash_password(user_data.password)
    new_user_data = UserAdd(email=user_data.email, password=hashed_password)
    async with async_session_maker() as session:
        is_exist = await UserRepositories(session).check_exist(user_data.email)
        if is_exist:
            return {"result": "User are already registered"}
        await UserRepositories(session).add(new_user_data)
        await session.commit()
        return {"result": "OK"}

@router.post("/login")
async def login_user(data: UserRequestAdd, response: Response):
    async with async_session_maker() as session:
        user = await UserRepositories(session).get_user_with_hash_passwort(
            email=data.email,
        )
        if not user:
            return HTTPException(status_code=401, detail="User does not exist")

        if not verify_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        access_token = create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}
