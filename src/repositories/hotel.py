from datetime import date
from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.hotel import HotelOrm
from src.models.room import RoomOrm
from src.schemas.hotel import Hotel
from src.repositories.utils import rooms_id_for_booking


class HotelRepository(BaseRepository):
    model = HotelOrm
    schema = Hotel


    # async def get_all(
    #         self,
    #         title,
    #         location,
    #         per_page,
    #         offset
    # ):
    #     query = select(self.model)
    #     if title is not None:
    #         query = query.filter(func.lower(self.model.title).contains(title.lower()))
    #     if location is not None:
    #         query = query.filter(func.lower(self.model.location).contains(location.lower()))
    #     query = query.limit(per_page).offset(offset)
    #     result = await self.session.execute(query)
    #     return [
    #         self.schema.model_validate(model, from_attributes=True)
    #         for model in result.scalars().all()
    #     ]

    async def filtered_by_time(
            self,
            date_from: date,
            date_to: date
    ):
        rooms_id_to_get = rooms_id_for_booking(date_from, date_to)
        hotels_id = (
            select(RoomOrm.hotel_id)
            .select_from(RoomOrm)
            .filter(RoomOrm.id.in_(rooms_id_to_get))
        )
        return await self.get_filtered(HotelOrm.id.in_(hotels_id))


