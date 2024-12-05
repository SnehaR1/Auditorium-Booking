from app.schemas.auditorium import AuditoriumSchema,AuditoriumResponseSchema
from fastapi import APIRouter, HTTPException,Depends,Query,Header
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List
from app.models.auditorium import Auditorium

router = APIRouter()

@router.get("/", response_model=List[AuditoriumResponseSchema])
def home(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100),db:Session=Depends(get_db), X_Custom_Header : str = Header(None)):
    try:
        skip = (page - 1) * size
        limit = size
        auditoriums = db.query(Auditorium).offset(skip).limit(limit).all()
        return auditoriums
    
    except Exception as e:
        raise HTTPException(status_code=400,detail={"message":str(e)})
   
    

@router.post("/")
def add_auditorium(auditorium:AuditoriumSchema,db:Session=Depends(get_db),X_Custom_Header : str = Header(None)):
    try:
        new_auditorium=Auditorium(**auditorium.model_dump())
        db.add(new_auditorium)
        db.commit()
        db.refresh(new_auditorium)
        return {"Message":"Auditorium added Successfully!","auditorium":new_auditorium}
    except ValidationError as e:
        raise HTTPException(status_code=422,detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400,detail={"message": f"Something went wrong while adding the auditorium.{str(e)}", "data": None})

@router.put("/{id}/")
def update_auditorium(id:int,auditorium:AuditoriumSchema,db:Session=Depends(get_db),X_Custom_Header : str = Header(None)):
    try:
        update_auditorium=db.query(Auditorium).filter(id==id).first()
        if update_auditorium is None:
            raise HTTPException(status_code=400,detail={"message":"No auditorium with th provided id exists!","data": None})
        else:
            update_auditorium.name = auditorium.name
            update_auditorium.seating = auditorium.seating
            update_auditorium.booking_charge = auditorium.booking_charge
            db.commit()
            db.refresh(update_auditorium)
            return {"message":"Auditorium updated!","updated_auditorium":update_auditorium}
    

    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400,detail={"message":f"Something went wrong!","data":None})

@router.delete("/{id}/")
def delete_auditorium(id:int,db:Session=Depends(get_db),X_Custom_Header : str = Header(None)):
    try:
        delete_auditorium=db.query(Auditorium).filter(Auditorium.id==id).first()
        if delete_auditorium is None:
            raise HTTPException(status_code=400,detail={"message":"No auditorium with th provided id exists!","data":None})
        else:
            db.delete(delete_auditorium)
            db.commit()
            return {"message":"Auditorium information deleted successfully!"}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400,detail={"message":"Something went wrong while deleteing the auditorium's availability ","data":None})