
from sqlalchemy import String,Integer,Column,text,ForeignKey,Date,Time,Boolean, Numeric,Interval,TIMESTAMP,Enum as SQLAlchemyEnum,UniqueConstraint
from app.database import Base
from sqlalchemy.orm import relationship
from enum import Enum
from sqlalchemy.sql import func




class PaymentStatusEnum(str, Enum):
    pending = "pending"
    completed = "completed"

class BookingStatusEnum(str,Enum):
    booked="booked"
    cancelled="cancelled"



class Booking(Base):

    __tablename__="bookings"

    id=Column(Integer,primary_key=True,nullable=False,index=True)
    auditorium_id=Column(Integer,ForeignKey("auditoriums.id",ondelete="CASCADE"),index=True)
    slot_id=Column(Integer,ForeignKey("slots.id",ondelete="CASCADE"),index=True)
    payment_status=Column(SQLAlchemyEnum(PaymentStatusEnum),nullable=False, default=PaymentStatusEnum.pending)
    booked_day=Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())
    status=Column(String,nullable=False,default=BookingStatusEnum.booked)
    requested_seats=Column(Integer,nullable=False,default=0)

    
    