# demo_output.py
import json
from spatial_engine import Spatial3DEngine

engine = Spatial3DEngine(default_floor_height=3.0)

# Sample building coordinates in Mangaluru [lng, lat]
mangaluru_footprint = [
    (74.85600, 12.87000),
    (74.85610, 12.87000),
    (74.85610, 12.87010),
    (74.85600, 12.87010)
]

# Generate a parcel on Floor 3 with ground elevation at 15.0m
record = engine.build_3d_property_record(
    ulpin="KA-MNG-P0001-B01-F03-U01",
    boundary_coordinates=mangaluru_footprint,
    base_ground_elevation=15.0,
    floor_height=3.0
)

# Print human-readable JSON
print(json.dumps(record, indent=2))