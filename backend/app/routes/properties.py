from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.utils import property_to_dict


router = APIRouter(
    prefix="/properties",
    tags=["Properties"]
)


# --------------------------------
# REGISTER PROPERTY
# --------------------------------

@router.post(
    "",
    response_model=dict,
    status_code=status.HTTP_201_CREATED
)
def register_property(
    data: schemas.PropertyCreate,
    db: Session = Depends(get_db)
):

    property_data = crud.create_property(
        db=db,
        state=data.state,
        district=data.district,
        location=data.location
    )

    return property_to_dict(property_data)


# --------------------------------
# GET ALL PROPERTIES
# --------------------------------

@router.get("")
def get_all_properties(
    db: Session = Depends(get_db)
):

    properties = crud.get_properties(db)

    return {
        "properties": [
            property_to_dict(property_data)
            for property_data in properties
        ],
        "count": len(properties)
    }


# --------------------------------
# GET PROPERTY BY ULPIN
# --------------------------------

@router.get("/ulpin/{ulpin}")
def get_property_by_ulpin(
    ulpin: str,
    db: Session = Depends(get_db)
):

    property_data = crud.get_property_by_ulpin(
        db,
        ulpin
    )

    if property_data is None:

        raise HTTPException(
            status_code=404,
            detail="Property not found"
        )

    return property_to_dict(property_data)


# --------------------------------
# GET PROPERTY BY ID
# --------------------------------

@router.get("/{property_id}")
def get_property(
    property_id: int,
    db: Session = Depends(get_db)
):

    property_data = crud.get_property(
        db,
        property_id
    )

    if property_data is None:

        raise HTTPException(
            status_code=404,
            detail="Property not found"
        )

    return property_to_dict(property_data)