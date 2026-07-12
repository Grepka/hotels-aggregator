from fastapi import APIRouter, Body


from src.schemas.bookings import Booking, BookingAdd, BookingAddRequest
from src.api.dependencies import UserIdDep,DBDep


router = APIRouter(prefix="/bookings", tags=["Бронирование"])


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