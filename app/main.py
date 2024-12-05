from fastapi import FastAPI
from .crud import auditorium,slot,booking
from app.database import Base,engine
from app.middleware.custom_middleware import CustomMiddleware
from app.models.booking import Booking
from app.models.slot import Slot
from app.models.auditorium import Auditorium


Base.metadata.create_all(bind=engine)


app = FastAPI()
app.add_middleware(CustomMiddleware)

app.include_router(auditorium.router, prefix="/auditorium", tags=["Auditorium"])
app.include_router(slot.router, prefix="/slot", tags=["Slot"])
app.include_router(booking.router, prefix="/booking", tags=["Booking"])





