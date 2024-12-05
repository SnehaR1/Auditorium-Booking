from pydantic import BaseModel ,Field, field_validator,ConfigDict
ConfigDict
from app.models.booking import PaymentStatusEnum
from fastapi import HTTPException,Depends
from datetime import date, time,timedelta
from app.database import get_db
from sqlalchemy.orm import Session
from decimal import Decimal
from app.models.booking import Booking
from app.models.slot import Slot


class BookingSchema(BaseModel):
    requested_seats:int=Field(...,ge=0)
    payment_status:PaymentStatusEnum =  PaymentStatusEnum.pending
   

    model_config = ConfigDict(from_attributes=True)

    @field_validator("requested_seats")
    def check_requested_seats(value):
        if value<=0:
            raise ValueError("Provide valid seat numbers")
        return value


    
