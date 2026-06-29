from fastapi import APIRouter, Query


from src.database import async_session_maker
from src.schemas.hotel import Hotel, HotelPATCH
from src.api.dependencies import PaginationDepends
from src.models.hotel import HotelOrm
from src.repositories.hotel import HotelRepository


router = APIRouter(prefix="/hotels", tags=["Отели"])


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
        return {"result": "ok", "data": hotel}

@router.put("/{hotel_id}")
async def reload_hotel(hotel_id: int, hotels_data: Hotel) -> dict:
    global hotels_list
    for hotel in hotels_list:
        if hotel["id"] == hotel_id:
            hotel["name"] = hotels_data.name
            hotel["city"] = hotels_data.city
            return {"result": "ok"}

    return {"result": "not ok"}

@router.patch(
    "/{hotel_id}",
        summary="Частичное обновление данных об отеле",
        description="Тут частично обновляем данные об отеле"
)
async def edit_hotel(hotel_id: int, hotels_data: HotelPATCH) -> dict:
    global hotels_list
    hotel = [hotel for hotel in hotels_list if hotel["id"] == hotel_id][0]
    if hotel is not None:
        if hotels_data.name is not None:
            hotel["name"] = hotels_data.name
        if hotels_data.city is not None:
            hotel["city"] = hotels_data.city
        return {"result": "ok"}
    return {"result": "not ok"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    global hotels_list
    hotels_list = [hotel for hotel in hotels_list if hotel["id"] != hotel_id]
    return {"result": "ok"}