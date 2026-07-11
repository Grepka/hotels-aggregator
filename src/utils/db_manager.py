from src.repositories.hotel import HotelRepository
from src.repositories.user import UserRepositories
from src.repositories.room import RoomRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory


    async def __aenter__(self):
        self.session = self.session_factory()

        self.hotels = HotelRepository(self.session)
        self.users = UserRepositories(self.session)
        self.rooms = RoomRepository(self.session)

        return self

    async def __aexit__(self):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()