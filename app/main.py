from fastapi import Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app import models

from sqlalchemy import select

from app.schemas import SalonInput, SalonOutput, StylistInput, StylistOutput


# create_all creates any missing tables and never wipes existing ones. It runs whenever main.py is imported, including when pytest imports it, which is what creates fullchair.db
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(title="FullChair")


# first endpoint
@app.get("/health")
def health():
    return {"ok": True}


#define route in route decorator 
# status_code parameter defines the HTTP status code that the server returns when the endpoint finishes successfully.
# The response_model parameter tells FastAPI exactly how to format, filter, and validate the data leaving your API. It uses Pydantic models to define the shape of the outgoing data.
@app.post("/salons", response_model=SalonOutput, status_code=201)
# This endpoint creates a new salon in the database, foollowing the 
# schema defined by SalonInput, and a new session for this endpoint 
def create_salon(salon: SalonInput, db: Session = Depends(get_db)):   
    salon=models.Salon(name=salon.name)
    db.add(salon)
    db.commit()
    db.refresh(salon)
    return salon

@app.post("/salons/stylists", response_model=StylistOutput, status_code=201)
def createStylist(stylist: StylistInput, db: Session=Depends(get_db)):
    stylist=models.Stylist(name=stylist.name, salon_id=stylist.salon_id)

