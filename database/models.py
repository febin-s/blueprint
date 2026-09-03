from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    property_code = Column(String(50), unique=True, nullable=False)
    owner_name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    buildings = relationship(
        "Building",
        back_populates="property",
        cascade="all, delete-orphan"
    )


class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)

    property_id = Column(
        Integer,
        ForeignKey("properties.id"),
        nullable=False
    )

    building_name = Column(String(100), nullable=False)
    building_number = Column(String(50))
    total_floors = Column(Integer, default=1)
    basement_levels = Column(Integer, default=0)
    building_height = Column(Float, default=0.0)

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

    building_id = Column(
        Integer,
        ForeignKey("buildings.id"),
        nullable=False
    )

    floor_number = Column(Integer, nullable=False)
    floor_name = Column(String(100), nullable=False)
    floor_height = Column(Float, default=3.0)
    vertical_position = Column(Float, default=0.0)

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

    floor_id = Column(
        Integer,
        ForeignKey("floors.id"),
        nullable=False
    )

    unit_number = Column(String(50), nullable=False)
    unit_type = Column(String(50), default="Flat")
    area = Column(Float, nullable=False)

    ulpin = Column(
        String(100),
        unique=True,
        index=True,
        nullable=False
    )

    latitude = Column(Float)
    longitude = Column(Float)
    vertical_position = Column(Float, default=0.0)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    floor = relationship(
        "Floor",
        back_populates="units"
    )