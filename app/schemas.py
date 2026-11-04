# FILE: Your models describe the database. Schemas describe 
# what goes in and out of the API. 
# They’re separate on purpose: you don’t always want users sending or seeing everything in the database.

# Pydantic is a library that checks data. You describe what your data should look like, using Python types, and Pydantic makes sure incoming data actually matches. If it doesn’t, Pydantic rejects it with a clear error.
# FastAPI is built on top of Pydantic, so they work together automatically.
from pydantic import BaseModel, ConfigDict, Field

class SalonInput(BaseModel):
    name: str = Field(min_length=1, max_length=100)

class SalonOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    id: int

#what goes in and out of stylist input field
class StylistInput(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    
class StylistOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    id: int
    

# service
class ServiceInput(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price_cents: int
    duration_minutes: int

class ServiceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    price_cents: int
    duration_minutes: int
    id: int

# client 
class ClientInput(BaseModel):
    name: str=Field(min_length=1, max_length=100)
    phone: str=Field(min_length=1, max_length=20)

class ClientOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    phone: str
    id: int

# appointment
class AppointmentInput(BaseModel):
    stylist_id: int
    client_id: int
    service_id: int
    start_at: str
    end_at: str  
class AppointmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    stylist_id: int
    client_id: int
    service_id: int
    start_at: str
    end_at: str
    status: str
    id: int





    




