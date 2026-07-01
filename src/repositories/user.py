from src.repositories.base import BaseRepository
from src.models.user import UserOrm
from src.schemas.user import User


class UserRepositories(BaseRepository):
    model = UserOrm
    schema = User