from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect

from app import crud
from app.database import get_db


router = APIRouter(
    prefix="/properties",
    tags=["3D"]
)


def serialize_object(obj, visited=None):
    """
    Convert SQLAlchemy objects into JSON-friendly data.
    Relationships are automatically included.
    """

    if visited is None:
        visited = set()

    if obj is None:
        return None

    object_id = id(obj)

    if object_id in visited:
        return None

    visited.add(object_id)

    result = {}

    # Normal database columns
    mapper = inspect(obj).mapper

    for column in mapper.columns:
        value = getattr(obj, column.key, None)

        # Convert database names to frontend-friendly names
        key = column.key

        if key == "id":
            key = "id"

        result[key] = value

    # Relationships
    for relationship in mapper.relationships:
        relation_name = relationship.key
        related = getattr(obj, relation_name, None)

        if related is None:
            continue

        if relationship.uselist:
            result[relation_name] = []

            for item in related:
                serialized = serialize_object(
                    item,
                    visited.copy()
                )

                if serialized is not None:
                    result[relation_name].append(serialized)

        else:
            serialized = serialize_object(
                related,
                visited.copy()
            )

            if serialized is not None:
                result[relation_name] = serialized

    return result


@router.get("/{property_id}/3d")
def get_3d_property(
    property_id: int,
    db: Session = Depends(get_db)
):
    property_obj = crud.get_property(
        db,
        property_id
    )

    if property_obj is None:
        raise HTTPException(
            status_code=404,
            detail="Property not found"
        )

    data = serialize_object(property_obj)

    return {
        "propertyId": data.get("id"),
        "ulpin": data.get("ulpin"),
        "state": data.get("state"),
        "district": data.get("district"),
        "location": data.get("location"),
        "building": data.get("buildings", []),
        "floors": data.get("floors", []),
        "units": data.get("units", [])
    }