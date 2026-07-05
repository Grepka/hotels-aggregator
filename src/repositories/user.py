from pydantic import EmailStr
from sqlalchemy import select, exists

from src.repositories.base import BaseRepository
from src.models.user import UserOrm
from src.schemas.user import User, UserWithHashPassword


class UserRepositories(BaseRepository):
    model = UserOrm
    schema = User

    async def check_exist(self, email: EmailStr) -> bool:
        stmt = select(exists().where(self.model.email == email))
        return await self.session.scalar(stmt)

    async def get_user_with_hash_passwort(self, email: EmailStr):
        stmt = select(self.model).where(self.model.email == email)
        result = await self.session.execute(stmt)
        return UserWithHashPassword.model_validate(
            result.scalar_one_or_none(),
            from_attributes=True
        )


