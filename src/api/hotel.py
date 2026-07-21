from datetime import date
from fastapi import APIRouter, Query, Body


from src.schemas.hotel import HotelAdd, HotelPatch
from src.api.dependencies import PaginationDepends, DBDep


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{hotel_id}")
async def get_hotel_by_id(hotel_id: int, db: DBDep):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    return {"result": "OK", "data": hotel}

@router.get("")
async def get_hotels(
        pagination: PaginationDepends,
        db: DBDep,
        date_from: date,
        date_to: date,
        # title: str=Query(default=None, description="Название отеля"),
        # location: str=Query(default=None, description="Адрес"),
):
        per_page = pagination.per_page or 5
        return await db.hotels.filtered_by_time(
            date_from=date_from,
            date_to=date_from
        )



@router.post("")
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body()):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"result": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def reload_hotel(hotel_id: int, hotels_data: HotelAdd, db: DBDep):
    await db.hotels.edit(hotels_data, exclude_unset=False, id=hotel_id)
    await db.commit()
    return {"result": "OK"}

@router.patch(
    "/{hotel_id}",
        summary="Частичное обновление данных об отеле",
        description="Тут частично обновляем данные об отеле"
)
async def edit_hotel(hotel_id: int, hotels_data: HotelPatch, db: DBDep):
    await db.hotels.edit(hotels_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"result": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"result": "OK"}
