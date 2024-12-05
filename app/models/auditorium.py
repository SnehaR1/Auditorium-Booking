
from sqlalchemy import String,Integer,Column, Numeric
from app.database import Base
from sqlalchemy.orm import relationship

class Auditorium(Base):
    __tablename__="auditoriums"

    id=Column(Integer,primary_key=True,nullable=False,index=True)
    name=Column(String,nullable=False,index=True)
    seating=Column(Integer,nullable=False)
    booking_charge = Column(Numeric(5, 2), nullable=False)

    slots = relationship("Slot", back_populates="auditorium")


