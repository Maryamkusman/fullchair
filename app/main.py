from fastapi import Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app import models

from sqlalchemy import select

from app.schemas import SalonInput, SalonOut, SalonOut, StylistInput, StylistOut 

#A rough guide: codes in the 200s mean success, 400s mean the client made a mistake, and 500s mean the server broke.
# create_all creates any missing tables and never wipes existing ones. It runs whenever main.py is imported, including when pytest imports it, which is what creates fullchair.db
# “Before running this endpoint, call get_db() and pass me what it gives back.” That’s a database session.
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(title="FullChair")


# first endpoint
@app.get("/health")
def health():
    return {"ok": True}

#salons 

#create a salon
@app.post("/salons", response_model=SalonOut, status_code=201)
def create_salon(salon: SalonInput, db: Session = Depends(get_db)):
    salon = models.Salon(name=salon.name)
    db.add(salon)
    db.commit()
    db.refresh(salon)
    return salon

#list all salons
@app.get("/salons", response_model=list[SalonOut])
def list_salons(db: Session = Depends(get_db)):
    return db.scalars(select(models.Salon).order_by(models.Salon.id)).all()


# get a salon by id 
@app.get("/salons/{salon_id}", response_model=SalonOut)
def get_salon(salon_id: int, db: Session = Depends(get_db)):
    salon = db.get(models.Salon, salon_id)
    if salon is None:
        raise HTTPException(status_code=404, detail="Salon not found")
    return salon

# stylist endpoints
@app.post("/salons/{salon_id}/stylists", response_model=StylistOut, status_code=201)
def create_stylist(salon_id: int, stylist_in: StylistInput, db: Session = Depends(get_db)):
    salon = db.get(models.Salon, salon_id)
    if salon is None:
        raise HTTPException(status_code=404, detail="Salon not found")
    stylist = models.Stylist(name=stylist_in.name, salon=salon)
    db.add(stylist)
    db.commit()
    db.refresh(stylist)
    return stylist


@app.get("/salons/{salon_id}/stylists", response_model=list[StylistOut])
def list_stylists(salon_id: int, db: Session = Depends(get_db)):
    salon = db.get(models.Salon, salon_id)
    if salon is None:
        raise HTTPException(status_code=404, detail="Salon not found")
    return salon.stylists

# appointment endpoints
