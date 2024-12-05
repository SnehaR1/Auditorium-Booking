from sqlalchemy import Integer,Column,ForeignKey,Date,Time,Enum as SQLAlchemyEnum,UniqueConstraint,String
from app.database import Base
from sqlalchemy.orm import relationship
from enum import Enum



class Slot(Base):

    __tablename__="slots"

    id=Column(Integer,primary_key=True,nullable=False,index=True)
    auditorium_id=Column(Integer,ForeignKey("auditoriums.id"),index=True)
    date = Column(Date, nullable=False,index=True)
    slot_name=Column(String,nullable=False,index=True)
  
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    auditorium= relationship("Auditorium", back_populates="slots")

    __table_args__ = (
        UniqueConstraint('auditorium_id', 'date',"start_time", name='unique_slot'),
    )
