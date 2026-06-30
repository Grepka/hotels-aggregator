from fastapi import APIRouter, Query


from src.database import async_session_maker
from src.schemas.hotel import Hotel, HotelPATCH
from src.api.dependencies import PaginationDepends
from src.repositories.hotel import HotelRepository


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{hotel_id}")
async def get_hotel_by_id(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await HotelRepository(session).get_one_or_none(id=hotel_id)
        return {"result": "OK", "data": hotel}

@router.get("")
async def get_hotels(
        pagination: PaginationDepends,
        title: str=Query(default=None, description="Название отеля"),
        location: str=Query(default=None, description="Адрес"),
):
    async with async_session_maker() as session:
        per_page = pagination.per_page or 5
        return await HotelRepository(session).get_all(
            title=title,
            location=location,
            per_page=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.post("")
async def create_hotel(hotel_data: Hotel):
    async with async_session_maker() as session:
        hotel = await HotelRepository(session).add(hotel_data)
        await session.commit()
        return {"result": "OK", "data": hotel}

@router.put("/{hotel_id}")
async def reload_hotel(hotel_id: int, hotels_data: Hotel):
    async with async_session_maker() as session:
        await HotelRepository(session).edit(hotels_data, exclude_unset=False, id=hotel_id)
        await session.commit()
        return {"result": "OK"}

@router.patch(
    "/{hotel_id}",
        summary="Частичное обновление данных об отеле",
        description="Тут частично обновляем данные об отеле"
)
async def edit_hotel(hotel_id: int, hotels_data: HotelPATCH):
    async with async_session_maker() as session:
        await HotelRepository(session).edit(hotels_data, exclude_unset=True, id=hotel_id)
        await session.commit()
        return {"result": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelRepository(session).delete(id=hotel_id)
        await session.commit()
        return {"result": "OK"}
