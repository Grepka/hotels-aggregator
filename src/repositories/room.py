from datetime import date


from src.repositories.base import BaseRepository
from src.models.room import RoomOrm
from src.schemas.room import Room
from src.repositories.utils import rooms_id_for_booking


class RoomRepository(BaseRepository):
    model = RoomOrm
    schema = Room

    async def filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        return await self.get_filtered(RoomOrm.id.in_(rooms_id_for_booking(date_from, date_to, hotel_id)))