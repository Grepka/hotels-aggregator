from fastapi import APIRouter, Body


from src.database import async_session_maker
from src.schemas.room import Room, RoomAdd, RoomsPatch, RoomAddRequest, RoomsPatchRequest
from src.repositories.room import RoomRepository


router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room_by_id(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        room = await RoomRepository(session).get_one_or_none(id=room_id)
        return {"result": "OK", "data": room}


@router.get("/{hotel_id}/rooms/")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        rooms = await RoomRepository(session).get_filtered(hotel_id=hotel_id)
        return {"result": "OK", "data": rooms}


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomRepository(session).add(_room_data)
        await session.commit()
        return {"result": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def reload_room(hotel_id: int, room_id: int, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=False))
    async with async_session_maker() as session:
        room = await RoomRepository(session).edit(
            id=room_id,
            exclude_unset=False,
            data=_room_data
        )
        await session.commit()
        return {"result": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def edit_room(hotel_id: int, room_id: int, room_data: RoomsPatchRequest = Body()):
    _room_data = RoomsPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        room = await RoomRepository(session).edit(
            id=room_id,
            exclude_unset=True,
            data=_room_data
        )
        await session.commit()
        return {"result": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
        return {"result": "OK"}