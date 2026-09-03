from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db


router = APIRouter(
    prefix="/properties",
    tags=["Buildings"]
)


@router.post(
    "/{property_id}/buildings",
    status_code=status.HTTP_201_CREATED
)
def add_building(
    property_id: int,
    data: schemas.BuildingCreate,
    db: Session = Depends(get_db)
):
    # Check if property exists
    property_data = crud.get_property(db, property_id)

    if property_data is None:
        raise HTTPException(
            status_code=404,
            detail="Property not found"
        )

    # Create building
    building = crud.create_building(
        db=db,
        property_id=property_id,
        data=data
    )

    return {
        "message": "Building added successfully",
        "buildingId": building.id,
        "propertyId": property_id,
        "name": building.name,
        "buildingType": building.building_type,
        "address": building.address,
        "latitude": building.latitude,
        "longitude": building.longitude,
        "height": building.height
    }