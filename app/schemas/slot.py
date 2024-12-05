from pydantic import BaseModel, field_validator,ConfigDict
from datetime import date, time
from fastapi import HTTPException

class SlotSchema(BaseModel):

    date:date
    slot_name:str
    start_time:time
    end_time:time


    model_config = ConfigDict(from_attributes=True)


    @field_validator("date")
    def check_date(cls,value):
        if not value:
            raise ValueError("Please provide the date!")

        if value<date.today():
            raise ValueError("Adding slot for the selected day is not possible! Please pick another day!")
        return value

  

    @field_validator('start_time')
    def check_start_time(cls, value):
        if not value:
            raise ValueError("Please provide the start time!")
        return value
    
    @field_validator("end_time")
    def check_end_time(cls,value):
        if not value:
            raise ValueError("Please provide the end time")
        return value
    
    
    
 
    

   

        