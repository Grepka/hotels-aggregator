from fastapi import APIRouter, HTTPException, Response, status

from src.database import async_session_maker
from src.schemas.user import UserRequestAdd, UserAdd
from src.repositories.user import UserRepositories
from src.service.auth import AuthService
from src.api.dependencies import UserIdDep


router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация пользователей"])


@router.post("/register")
async def create_user(user_data: UserRequestAdd):
    hashed_password = AuthService().hash_password(user_data.password)
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

        if not AuthService().verify_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return{"result": "OK"}


@router.post("/me")
async def me(user_id: UserIdDep):
    async with async_session_maker() as session:
        return await UserRepositories(session).get_one_or_none(id=user_id)
