
from fastapi import APIRouter, HTTPException,Depends,Header,Query
from app.schemas.slot import SlotSchema
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.auditorium import Auditorium
from app.models.slot import Slot
from datetime import timedelta,datetime


router = APIRouter()



@router.post("/{auditorium_id}/")
def add_slot(auditorium_id: int, slot: SlotSchema, db: Session = Depends(get_db),X_Custom_Header : str = Header(None)):
    try:
        start_time = slot.start_time
        end_time = slot.end_time
        date = slot.date
        
        auditorium = db.query(Auditorium).filter(Auditorium.id == auditorium_id).first()
        if not auditorium:
            raise HTTPException(status_code=400, detail={"message": "No auditorium with the given id exists", "data": None})

        all_slots = db.query(Slot).filter(Slot.auditorium_id == auditorium_id, Slot.date == slot.date).all()

        start_datetime = datetime.combine(date, start_time)
        end_datetime = datetime.combine(date, end_time)

        for existing_slot in all_slots:
            existing_start = datetime.combine(date, existing_slot.start_time)
            existing_end = datetime.combine(date, existing_slot.end_time)

            if start_datetime == existing_start:
                raise HTTPException(status_code=400, detail={"message": f"Slot with that start time already exists! Try booking for {(existing_end + timedelta(minutes=15)).time()}", "data": None})

            if start_datetime < existing_end and end_datetime > existing_start:
                raise HTTPException(status_code=400, detail={"message": f"Provided time overlaps with an existing slot! Try booking for {(existing_end + timedelta(minutes=15)).time()}", "data": None})


            if start_datetime < existing_end + timedelta(minutes=15) and existing_start<start_datetime:
                next_slot_exists = db.query(Slot).filter(Slot.start_time == (existing_end + timedelta(minutes=15)).time()).first()
                if next_slot_exists:
                    raise HTTPException(status_code=400, detail={"message": "Provided start time conflicts with an existing slot. Please try again with a new start time!", "data": None})
                raise HTTPException(status_code=400, detail={"message": f"Provided start time conflicts with an existing slot. Try booking for {existing_end + timedelta(minutes=15)}", "data": None})

            if end_datetime > existing_start - timedelta(minutes=15) and end_datetime <= existing_start:
                next_slot_exists = db.query(Slot).filter(Slot.start_time == (existing_end + timedelta(minutes=15)).time()).first()
                if next_slot_exists:
                    raise HTTPException(status_code=400, detail={"message": "Provided end time conflicts with an existing slot. Please try again with a new start time!", "data": None})
                raise HTTPException(status_code=400, detail={"message": f"Provided end time conflicts with an existing slot. Try adding for {existing_start - timedelta(minutes=15)}", "data": None})

        slot_data = slot.dict()
        slot_data["auditorium_id"] = auditorium_id

        new_slot = Slot(**slot_data)
        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)

        return {"message": "Slot for the Auditorium added!", "slot": new_slot}

    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"message": str(e), "data": None})
    except Exception as e:
        raise HTTPException(status_code=400, detail={"message": f"Something went wrong while adding the auditorium's availability. ", "data": None})
