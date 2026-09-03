from pydantic import BaseModel
from typing import Optional

# Property Schema
class PropertyCreate(BaseModel):
    state: str
    district: str
    location: str

class PropertyResponse(BaseModel):
    propertyId: int
    ulpin: str
    state: str
    district: str
    location: str

    class Config:
        from_attributes = True


# Building Schema
class BuildingCreate(BaseModel):
    name: str
    building_type: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    height: Optional[float] = None


# Floor Schema
class FloorCreate(BaseModel):
    floor_number: int
    name: str
    height: float


# Unit Schema
class UnitCreate(BaseModel):
    unit_number: str
    unit_type: str
    area_sqft: float
    owner_name: str
    status: str