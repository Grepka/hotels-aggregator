from sqlalchemy import select, insert, func

from src.repositories.base import BaseRepository
from src.models.hotel import HotelOrm


class HotelRepository(BaseRepository):
    model = HotelOrm

    async def get_all(
            self,
            title,
            location,
            per_page,
            offset
    ):
        query = select(self.model)
        if title is not None:
            query = query.filter(func.lower(self.model.title).contains(title.lower()))
        if location is not None:
            query = query.filter(func.lower(self.model.location).contains(location.lower()))
        query = query.limit(per_page).offset(offset)
        result = await self.session.execute(query)
        return result.scalars().all()
