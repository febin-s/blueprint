from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db


router = APIRouter(
    prefix="/buildings",
    tags=["Floors"]
)


@router.post(
    "/{building_id}/floors",
    status_code=status.HTTP_201_CREATED
)
def add_floor(
    building_id: int,
    data: schemas.FloorCreate,
    db: Session = Depends(get_db)
):
    # Check whether building exists
    building = crud.get_building(
        db,
        building_id
    )

    if building is None:
        raise HTTPException(
            status_code=404,
            detail="Building not found"
        )

    # Create floor
    floor = crud.create_floor(
        db=db,
        building_id=building_id,
        data=data
    )

    return {
        "message": "Floor added successfully",
        "floorId": floor.id,
        "buildingId": building_id,
        "floorNumber": floor.floor_number,
        "name": floor.name,
        "height": floor.height
    }