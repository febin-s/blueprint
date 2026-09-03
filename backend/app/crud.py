from sqlalchemy.orm import Session

from app import models


# -----------------------------
# PROPERTY
# -----------------------------

def generate_ulpin(property_id: int, state: str, district: str):

    state_code = "".join(
        character for character in state.upper()
        if character.isalnum()
    )[:2]

    district_code = "".join(
        character for character in district.upper()
        if character.isalnum()
    )[:3]

    state_code = state_code.ljust(2, "X")
    district_code = district_code.ljust(3, "X")

    return f"ULP-{state_code}{district_code}-{property_id:06d}"


def create_property(
    db: Session,
    state: str,
    district: str,
    location: str
):

    property_data = models.Property(
        ulpin="PENDING",
        state=state.strip(),
        district=district.strip(),
        location=location.strip()
    )

    db.add(property_data)

    # Get database ID before generating ULPIN
    db.flush()

    property_data.ulpin = generate_ulpin(
        property_data.id,
        state,
        district
    )

    db.commit()
    db.refresh(property_data)

    return property_data


def get_property(
    db: Session,
    property_id: int
):

    return db.query(models.Property).filter(
        models.Property.id == property_id
    ).first()


def get_property_by_ulpin(
    db: Session,
    ulpin: str
):

    return db.query(models.Property).filter(
        models.Property.ulpin == ulpin.upper()
    ).first()


def get_properties(db: Session):

    return db.query(models.Property).order_by(
        models.Property.id.desc()
    ).all()


# -----------------------------
# BUILDING
# -----------------------------

def create_building(
    db: Session,
    property_id: int,
    data
):

    building = models.Building(
        property_id=property_id,
        name=data.name.strip(),
        building_type=data.building_type,
        address=data.address,
        latitude=data.latitude,
        longitude=data.longitude,
        height=data.height
    )

    db.add(building)
    db.commit()
    db.refresh(building)

    return building


def get_building(
    db: Session,
    building_id: int
):

    return db.query(models.Building).filter(
        models.Building.id == building_id
    ).first()


# -----------------------------
# FLOOR
# -----------------------------

def create_floor(
    db: Session,
    building_id: int,
    data
):

    floor = models.Floor(
        building_id=building_id,
        floor_number=data.floor_number,
        name=data.name,
        height=data.height
    )

    db.add(floor)
    db.commit()
    db.refresh(floor)

    return floor


def get_floor(
    db: Session,
    floor_id: int
):

    return db.query(models.Floor).filter(
        models.Floor.id == floor_id
    ).first()


# -----------------------------
# UNIT
# -----------------------------

def create_unit(
    db: Session,
    floor_id: int,
    data
):

    unit = models.Unit(
        floor_id=floor_id,
        unit_number=data.unit_number.strip(),
        unit_type=data.unit_type,
        area_sqft=data.area_sqft,
        owner_name=data.owner_name,
        status=data.status
    )

    db.add(unit)
    db.commit()
    db.refresh(unit)

    return unit