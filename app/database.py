from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine("sqlite:///fullchair.db", connect_args={"check_same_thread": False}, echo=True)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass