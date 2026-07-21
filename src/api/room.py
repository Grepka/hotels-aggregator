from datetime import date
from fastapi import APIRouter, Body, Query

from src.schemas.room import RoomAdd, RoomsPatch, RoomAddRequest, RoomsPatchRequest
from src.api.dependencies import DBDep


router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room_by_id(hotel_id: int, room_id: int, db: DBDep):
    room = await db.rooms.get_one_or_none(id=room_id)
    return {"result": "OK", "data": room}


@router.get("/{hotel_id}/rooms/")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(examples=["2026-10-12"]),
        date_to: date = Query(examples=["2026-10-15"]),
):
    rooms = await db.rooms.filtered_by_time(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to
    )
    return {"result": "OK", "data": rooms}


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()
    return {"result": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def reload_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        room_data: RoomAddRequest = Body()
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=False))
    room = await db.rooms.edit(
        id=room_id,
        exclude_unset=False,
        data=_room_data
    )
    await db.commit()
    return {"result": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def edit_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        room_data: RoomsPatchRequest = Body()):
    _room_data = RoomsPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    room = await db.rooms.edit(
        id=room_id,
        exclude_unset=True,
        data=_room_data
    )
    await db.commit()
    return {"result": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"result": "OK"}