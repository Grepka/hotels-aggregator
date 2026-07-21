from src.repositories.base import BaseRepository
from src.models.booking import BookingOrm
from src.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingOrm
    schema = Booking
