# FILE: Your models describe the database. Schemas describe 
# what goes in and out of the API. 
# They’re separate on purpose: you don’t always want users sending or seeing everything in the database.

# Pydantic is a library that checks data. You describe what your data should look like, using Python types, and Pydantic makes sure incoming data actually matches. If it doesn’t, Pydantic rejects it with a clear error.
# FastAPI is built on top of Pydantic, so they work together automatically.
from pydantic import BaseModel, ConfigDict, Field

#what can go into salon input field
class SalonInput(BaseModel):
    name: str =Field(min_length=1, max_length=100)

#what comes out of salon input field 
class SalonOut(BaseModel):
    #you can build this from an object’s attributes, not just a dictionary.
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    id: int

#what goes in and out of stylist input field
class StylistInput(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    salon_id: int

class StylistOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    id: int
    salon_id: int





