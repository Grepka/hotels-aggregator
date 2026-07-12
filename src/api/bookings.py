from fastapi import APIRouter, Body


from src.schemas.bookings import Booking, BookingAdd, BookingAddRequest
from src.api.dependencies import UserIdDep,DBDep


router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("")
async def get_bookings(db: DBDep):
    bookings = await db.bookings.get_all()
    return {"result": "OK", "data": bookings}

@router.get("/me")
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    bookings = await db.bookings.get_filtered(user_id=user_id)
    return {"result": "OK", "data": bookings}


@router.post("")
async def create_booking(user_id: UserIdDep, db: DBDep, booking_data: BookingAddRequest = Body()):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    _booking_data = BookingAdd(
        user_id=user_id,
        price = room.price,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"result": "OK", "data": booking}