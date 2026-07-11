from datetime import date
from sqlalchemy import BigInteger, ForeignKey, DateTime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column


from src.database import Base


class BookingOrm(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    room_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int]
    
    @hybrid_property
    def total_cost(self):
        return self.price * (self.date_from - self.date_to).days
