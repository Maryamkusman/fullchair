#FILE to connect to Database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# this is the connection to the database (halway to filing cabinet)
engine = create_engine("sqlite:///fullchair.db", connect_args={"check_same_thread": False}, echo=True)

# Create a new session for interacting with the database
SessionLocal = sessionmaker(autoflush=False, bind=engine)

# Parent class every table inherits from, so SQLAlchemy knows it exists
class Base(DeclarativeBase):
    pass

# Bridge between FastAPI and SQLAlchemy, each request gets a database session 
# Each request gets a fresh session (a clipboard), uses it, and the finally block always closes it afterward, even if something crashes. FastAPI calls this function for you whenever an endpoint asks for a database.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()