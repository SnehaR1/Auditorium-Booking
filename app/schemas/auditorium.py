from pydantic import BaseModel,field_validator,ConfigDict,Field
from decimal import Decimal

class AuditoriumSchema(BaseModel):
    name:str
    seating:int=Field(...,ge=0)
    booking_charge:Decimal=Field(...,ge=0)

    model_config = ConfigDict(from_attributes=True)
    
    @field_validator("name")
    def check_name(cls,value):
        if not value:
            raise ValueError("Name field is required!")
        if value and value.strip()=="":
            raise ValueError("Provide a Valid Name!")
        return value
    
    @field_validator("seating")
    def check_seating(cls,value):
        if value<0:
            raise ValueError("Provide a proper number for seats!")
        
        
        return value
    
class AuditoriumResponseSchema(BaseModel):
    id:int
    name:str
    seating:int
    booking_charge:Decimal
