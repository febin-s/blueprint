from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db


router = APIRouter(
    prefix="/floors",
    tags=["Units"]
)


@router.post(
    "/{floor_id}/units",
    status_code=status.HTTP_201_CREATED
)
def add_unit(
    floor_id: int,
    data: schemas.UnitCreate,
    db: Session = Depends(get_db)
):
    # Check whether floor exists
    floor = crud.get_floor(
        db,
        floor_id
    )

    if floor is None:
        raise HTTPException(
            status_code=404,
            detail="Floor not found"
        )

    # Create unit
    unit = crud.create_unit(
        db=db,
        floor_id=floor_id,
        data=data
    )

    return {
        "message": "Unit added successfully",
        "unitId": unit.id,
        "floorId": floor_id,
        "unitNumber": unit.unit_number,
        "unitType": unit.unit_type,
        "area": unit.area
    }