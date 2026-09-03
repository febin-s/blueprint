from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    ulpin = Column(String(32), unique=True, nullable=False, index=True)
    state = Column(String(100), nullable=False)
    district = Column(String(100), nullable=False)
    location = Column(String(255), nullable=False)

    buildings = relationship(
        "Building",
        back_populates="property",
        cascade="all, delete-orphan"
    )


class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)

    name = Column(String(150), nullable=False)
    building_type = Column(String(100))
    address = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    height = Column(Float)

    property = relationship(
        "Property",
        back_populates="buildings"
    )

    floors = relationship(
        "Floor",
        back_populates="building",
        cascade="all, delete-orphan"
    )


class Floor(Base):
    __tablename__ = "floors"

    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=False)

    floor_number = Column(Integer, nullable=False)
    name = Column(String(100))
    height = Column(Float)

    building = relationship(
        "Building",
        back_populates="floors"
    )

    units = relationship(
        "Unit",
        back_populates="floor",
        cascade="all, delete-orphan"
    )


class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    floor_id = Column(Integer, ForeignKey("floors.id"), nullable=False)

    unit_number = Column(String(50), nullable=False)
    unit_type = Column(String(100))
    area_sqft = Column(Float)
    owner_name = Column(String(150))
    status = Column(String(50))

    floor = relationship(
        "Floor",
        back_populates="units"
    )