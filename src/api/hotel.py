from typing import List
from fastapi import APIRouter, Query
from sqlalchemy import select, insert

from src.database import async_session_maker
from src.schemas.hotel import Hotel, HotelPATCH
from src.api.dependencies import PaginationDepends
from src.models.hotel import HotelOrm


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
        pagination: PaginationDepends,
        id: int = Query(default=None, description="ID"),
        name: str =  Query(default=None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelOrm)
        if id is not None:
            query = query.filter_by(id=id)
        if name is not None:
            query = query.filter_by(name=name)
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels


@router.post("")
async def create_hotel(hotel_data: Hotel):
    async with async_session_maker() as session:
        add_hotel_stm = insert(HotelOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stm)
        await session.commit()
    return {"result": "ok"}

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