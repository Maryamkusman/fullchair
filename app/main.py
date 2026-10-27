from fastapi import FastAPI
from app import models
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FullChair")


# first endpoint
@app.get("/health")
def health():
    return {"ok": True}

@app.get("/")
def root():
    return {"message": "Welcome to FullChair!"}