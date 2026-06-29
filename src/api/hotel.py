from typing import List
from fastapi import APIRouter, Query
from sqlalchemy import insert

from src.database import async_session_maker
from src.schemas.hotel import Hotel, HotelPATCH
from src.api.dependencies import PaginationDepends
from src.models.hotel import HotelOrm



router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels_list = [
    {"id": 1, "name": "Hilton Downtown", "city": "Dubai"},
    {"id": 2, "name": "Красная поляна", "city": "Sochi"},
    {"id": 3, "name": "Marriott Marina", "city": "Dubai"},
    {"id": 4, "name": "Grand Hotel", "city": "Moscow"},
    {"id": 5, "name": "Sea Breeze", "city": "Sochi"},
    {"id": 6, "name": "Sky Palace", "city": "Dubai"},
    {"id": 7, "name": "Nevsky Hotel", "city": "Saint Petersburg"},
    {"id": 8, "name": "Mountain View", "city": "Krasnaya Polyana"},
    {"id": 9, "name": "Royal Garden", "city": "Istanbul"},
    {"id": 10, "name": "Sunrise Resort", "city": "Antalya"},
    {"id": 11, "name": "Ocean Pearl", "city": "Miami"},
    {"id": 12, "name": "Golden Sands", "city": "Varna"},
    {"id": 13, "name": "Central Inn", "city": "Berlin"},
    {"id": 14, "name": "Imperial Hotel", "city": "Vienna"},
    {"id": 15, "name": "Palm Residence", "city": "Abu Dhabi"},
    {"id": 16, "name": "White Hills", "city": "Sochi"},
    {"id": 17, "name": "Blue Lagoon", "city": "Phuket"},
    {"id": 18, "name": "Comfort Stay", "city": "Prague"},
    {"id": 19, "name": "Green Park", "city": "London"},
    {"id": 20, "name": "Aurora Suites", "city": "Helsinki"},
]


@router.get("")
async def get_hotels(
        pagination: PaginationDepends,
        id: int = Query(default=None, description="ID"),
        name: str =  Query(default=None, description="Название отеля"),
) -> List:
    hotels_= []
    for hotel in hotels_list:
        if id and hotel["id"] != id:
            continue
        if name and hotel["name"] != name:
            continue
        hotels_.append(hotel)
    if pagination.page:
        start_index = (pagination.page - 1) * pagination.per_page
        end_index = start_index + pagination.per_page
        return hotels_[start_index:end_index]
    return hotels_

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