from src.repositories.base import BaseRepository
from src.models.room import RoomOrm
from src.schemas.room import Room


class RoomRepository(BaseRepository):
    model = RoomOrm
    schema = Room