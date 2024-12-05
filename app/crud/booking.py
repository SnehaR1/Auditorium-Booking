from fastapi import APIRouter, HTTPException,Depends,Query,Header
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas.booking import BookingSchema
from app.models.auditorium import Auditorium
from app.models.booking import Booking
from app.models.slot import Slot
from sqlalchemy import func
from typing import List

router = APIRouter()


@router.get("/")
def get_bookings(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100),db:Session=Depends(get_db),X_Custom_Header : str = Header(None)):
    try:
        skip = (page - 1) * size
        limit = size
        bookings = db.query(Booking).offset(skip).limit(limit).all()
        return bookings
    except Exception as e:
        raise HTTPException(status_code=400,detail={"message":str(e)})
   



@router.post("/{auditorium_id}/{slot_id}")
def add_booking(auditorium_id: int, slot_id: int, booking: BookingSchema, db: Session = Depends(get_db),X_Custom_Header : str = Header(None)):
    try:
        auditorium = db.query(Auditorium).filter(Auditorium.id == auditorium_id).first()
        if not auditorium:
            raise HTTPException(status_code=400, detail={"message": "No auditorium with the given id exists", "data": None})
        
        slot = db.query(Slot).filter(Slot.id == slot_id).first()
        if not slot:
            raise HTTPException(status_code=400, detail={"message": "No slot with the given id exists", "data": None})
        
        total_seats = auditorium.seating
        booked_seats = db.query(func.sum(Booking.requested_seats)).filter(Booking.auditorium_id == auditorium_id, Booking.slot_id == slot_id,Booking.status=='booked').scalar()
        available_seats = total_seats - booked_seats
        
        if available_seats < booking.requested_seats:  
            raise HTTPException(status_code=400, detail={"message": f"Booking for {booking.requested_seats} is not available"})
        
        requested_seats = booking.requested_seats
        booking_update = booking.dict()
        booking_update["status"] = "booked"
        booking_update["slot_id"] = slot_id
        booking_update["auditorium_id"] = auditorium_id
      
        
        new_booking = Booking(**booking_update)
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)
        
        return {"message": "Auditorium Booked Successfully!", "booking_information": new_booking}
    
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"message": str(e), "data": None})
    except Exception as e:
        raise HTTPException(status_code=400, detail={"message": f"Something went wrong while booking!", "data": None})

@router.patch("/{id}")
def cancel_booking(id:int,db:Session=Depends(get_db),X_Custom_Header : str = Header(None)):
    try:
        cancel_booking=db.query(Booking).filter(Booking.id==id).first()
        if not cancel_booking:
            return HTTPException(status_code=400,detail={"message":"No Booking with that ID!","data":None})
        
        cancel_booking.status="cancelled"
        db.commit()
        
        if cancel_booking.payment_status=="completed" and cancel_booking.event_date>date.today():
            return {"message":"Your booking has been cancelled successfully and the paid amount will be refunded"}
        return {"message":"Your booking has been cancelled successfully!"}
    except Exception as e:
        raise HTTPException(status_code=400,detail={"message":"Something went wrong while cancelling your booking!","data":None})


