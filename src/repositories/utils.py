from sqlalchemy import select, func


from src.models.booking import BookingOrm
from src.models.room import RoomOrm


def rooms_id_for_booking(
        date_to,
        date_from,
        hotel_id: int | None = None
):
    rooms_count = (
        select(
            BookingOrm.room_id, func.count("*").label("rooms_booked")
        )
        .select_from(BookingOrm)
        .filter(
            BookingOrm.date_from <= date_to,
            BookingOrm.date_to >= date_from,
        )
        .group_by(BookingOrm.room_id)
        .cte(name="rooms_count")
        )

    rooms_left_table = (
        select(
            RoomOrm.id.label("room_id"),
            (RoomOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left"),
        )
        .select_from(RoomOrm)
        .outerjoin(rooms_count, RoomOrm.id == rooms_count.c.room_id)
        .cte(name="rooms_left_table")
        )

    rooms_ids_for_hotel = (
        select(RoomOrm.id)
        .select_from(RoomOrm)
    )

    if hotel_id is not None:
        rooms_ids_for_hotel = rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)

    rooms_ids_for_hotel =  select(
        rooms_ids_for_hotel.subquery(name="rooms_ids_for_hotel")
    )

    rooms_id_to_get = (
        select(rooms_left_table.c.room_id)
        .select_from(rooms_left_table)
        .filter(
    rooms_left_table.c.rooms_left > 0,
            rooms_left_table.c.room_id.in_(rooms_ids_for_hotel),
        )
    )

    return rooms_id_to_get
