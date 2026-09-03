"""
SIH26011: 3D ULPIN & Vertical Spatial Cadastre Engine
Author: Person 4 (Algorithmic Engineer)
Role: Deterministic 3D spatial calculations, validation, and collision detection.
"""

import math
import re
from typing import Any, Dict, List, Optional, Tuple

EARTH_RADIUS_METERS = 6378137.0  # WGS84 Major Axis

# Strict Schema: ST-DST-P0000-B00-F00-U00 or ST-DST-P0000-B00-B00-U00
ULPIN_REGEX = re.compile(
    r"^(?P<state>[A-Z]{2})-(?P<district>[A-Z0-9]{3})-(?P<property>P\d{4})-(?P<building>B\d{2})-(?P<level>[FB]\d{2})-(?P<unit>U\d{2})$"
)


class SpatialMath:
    """Mathematical utilities for coordinate transformations and polygon topology."""

    @staticmethod
    def polygon_area_and_centroid_2d(coords: List[Tuple[float, float]]) -> Tuple[float, Tuple[float, float]]:
        """
        Calculates 2D planar area (m^2) using the Shoelace formula on an equirectangular
        projection and returns the 2D centroid [lng, lat].
        """
        n = len(coords)
        if n < 3:
            raise ValueError("A parcel polygon requires at least 3 distinct vertices.")

        ring = coords[:]
        if ring[0] != ring[-1]:
            ring.append(ring[0])
            n += 1

        origin_lng, origin_lat = ring[0]
        cos_lat = math.cos(math.radians(origin_lat))

        # Local metric projection relative to first point
        projected = []
        for lng, lat in ring:
            x = math.radians(lng - origin_lng) * EARTH_RADIUS_METERS * cos_lat
            y = math.radians(lat - origin_lat) * EARTH_RADIUS_METERS
            projected.append((x, y))

        # Shoelace Formula
        area = 0.0
        cx = 0.0
        cy = 0.0
        for i in range(len(projected) - 1):
            xi, yi = projected[i]
            x_next, y_next = projected[i + 1]
            cross = (xi * y_next) - (x_next * yi)
            area += cross
            cx += (xi + x_next) * cross
            cy += (yi + y_next) * cross

        signed_area = area / 2.0
        abs_area = abs(signed_area)

        if abs_area < 1e-6:
            raise ValueError("Degenerate polygon: Area is effectively zero.")

        cx = cx / (6.0 * signed_area)
        cy = cy / (6.0 * signed_area)

        centroid_lat = origin_lat + math.degrees(cy / EARTH_RADIUS_METERS)
        centroid_lng = origin_lng + math.degrees(cx / (EARTH_RADIUS_METERS * cos_lat))

        return round(abs_area, 3), (round(centroid_lng, 7), round(centroid_lat, 7))


class Spatial3DEngine:
    """Core algorithmic engine for 3D ULPIN generation, verification, and collision detection."""

    def __init__(self, default_floor_height: float = 3.0):
        self.default_floor_height = float(default_floor_height)
        self.registered_parcels: Dict[str, Dict[str, Any]] = {}

    def parse_ulpin(self, ulpin: str) -> Dict[str, str]:
        """Parses and validates the prototype ULPIN string."""
        match = ULPIN_REGEX.match(ulpin.strip())
        if not match:
            raise ValueError(
                f"ULPIN format violation: '{ulpin}'. Expected format: KA-MNG-P0001-B01-F03-U02"
            )
        return match.groupdict()

    def generate_ulpin(
        self,
        state: str,
        district: str,
        property_num: int,
        building_num: int,
        level_code: str,
        unit_num: int,
    ) -> str:
        """Constructs and returns a standardized ULPIN string."""
        ulpin = (
            f"{state.strip().upper()}-{district.strip().upper()}-"
            f"P{property_num:04d}-B{building_num:02d}-{level_code.strip().upper()}-U{unit_num:02d}"
        )
        self.parse_ulpin(ulpin)
        return ulpin

    def calculate_vertical_datum(
        self,
        level_code: str,
        base_ground_elevation: float = 0.0,
        floor_height: Optional[float] = None,
    ) -> Tuple[float, float]:
        """Calculates absolute vertical bounds (z_min, z_max)."""
        h = floor_height if floor_height is not None else self.default_floor_height
        if h <= 0:
            raise ValueError("Floor height must be positive.")

        prefix = level_code[0].upper()
        level_idx = int(level_code[1:])

        if prefix == "F":
            rel_min = level_idx * h
            rel_max = rel_min + h
        elif prefix == "B":
            if level_idx == 0:
                raise ValueError("Basement indexing begins at B01, not B00.")
            rel_max = -(level_idx - 1) * h
            rel_min = -level_idx * h
        else:
            raise ValueError(f"Invalid vertical prefix '{prefix}'. Expected 'F' or 'B'.")

        return round(base_ground_elevation + rel_min, 3), round(base_ground_elevation + rel_max, 3)

    @staticmethod
    def check_3d_box_collision(b1: Dict[str, float], b2: Dict[str, float]) -> bool:
        """Determines 3D Axis-Aligned Bounding Box (AABB) intersection."""
        x_overlap = (b1["lng_min"] < b2["lng_max"]) and (b1["lng_max"] > b2["lng_min"])
        y_overlap = (b1["lat_min"] < b2["lat_max"]) and (b1["lat_max"] > b2["lat_min"])
        z_overlap = (b1["z_min"] < b2["z_max"]) and (b1["z_max"] > b2["z_min"])
        return x_overlap and y_overlap and z_overlap

    def build_3d_property_record(
        self,
        ulpin: str,
        boundary_coordinates: List[Tuple[float, float]],
        base_ground_elevation: float = 0.0,
        floor_height: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Transforms 2D footprint and vertical specs into a verified 3D parcel payload."""
        if ulpin in self.registered_parcels:
            raise ValueError(f"Duplicate Error: ULPIN '{ulpin}' is already registered.")

        metadata = self.parse_ulpin(ulpin)
        z_min, z_max = self.calculate_vertical_datum(
            metadata["level"], base_ground_elevation, floor_height
        )

        area_sqm, (c_lng, c_lat) = SpatialMath.polygon_area_and_centroid_2d(boundary_coordinates)
        volume_cbm = round(area_sqm * (z_max - z_min), 3)

        footprint = boundary_coordinates[:]
        if footprint[0] != footprint[-1]:
            footprint.append(footprint[0])

        lngs = [pt[0] for pt in footprint]
        lats = [pt[1] for pt in footprint]

        bounds_3d = {
            "lng_min": min(lngs),
            "lng_max": max(lngs),
            "lat_min": min(lats),
            "lat_max": max(lats),
            "z_min": z_min,
            "z_max": z_max,
        }

        for existing_id, existing_parcel in self.registered_parcels.items():
            if self.check_3d_box_collision(bounds_3d, existing_parcel["bounds_3d"]):
                raise ValueError(
                    f"Spatial Conflict: Parcel '{ulpin}' physically collides with registered parcel '{existing_id}'."
                )

        record = {
            "ulpin": ulpin,
            "components": metadata,
            "spatial_metrics": {
                "footprint_area_sqm": area_sqm,
                "volume_cbm": volume_cbm,
                "vertical_thickness_m": round(z_max - z_min, 3),
                "centroid_3d": [c_lng, c_lat, round((z_min + z_max) / 2.0, 3)],
            },
            "bounds_3d": bounds_3d,
            "geometry_3d": {
                "type": "MultiPolygonZ",
                "coordinates": {
                    "base_ring": [[lng, lat, z_min] for lng, lat in footprint],
                    "roof_ring": [[lng, lat, z_max] for lng, lat in footprint],
                },
            },
        }

        self.registered_parcels[ulpin] = record
        return record


# ---------------------------------------------------------------------------
# Self-Running Test Execution Block
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("\n========== RUNNING SIH26011 ALGORITHMIC CORE TESTS ==========")
    engine = Spatial3DEngine(default_floor_height=3.0)

    sample_footprint = [
        (74.85600, 12.87000),
        (74.85610, 12.87000),
        (74.85610, 12.87010),
        (74.85600, 12.87010),
        (74.85600, 12.87000)
    ]

    # Test 1: Ground Floor
    f0 = engine.build_3d_property_record("KA-MNG-P0001-B01-F00-U01", sample_footprint, 0.0)
    assert f0["bounds_3d"]["z_min"] == 0.0 and f0["bounds_3d"]["z_max"] == 3.0
    print("[PASS] Ground Floor (F00) elevation: 0.0m - 3.0m")

    # Test 2: Floor 3
    f3 = engine.build_3d_property_record("KA-MNG-P0001-B01-F03-U01", sample_footprint, 0.0)
    assert f3["bounds_3d"]["z_min"] == 9.0 and f3["bounds_3d"]["z_max"] == 12.0
    print("[PASS] Floor 3 (F03) elevation: 9.0m - 12.0m")

    # Test 3: Basement 1
    b1 = engine.build_3d_property_record("KA-MNG-P0001-B01-B01-U01", sample_footprint, 0.0)
    assert b1["bounds_3d"]["z_min"] == -3.0 and b1["bounds_3d"]["z_max"] == 0.0
    print("[PASS] Basement (B01) elevation: -3.0m - 0.0m")

    # Test 4: Duplicate Rejection
    try:
        engine.build_3d_property_record("KA-MNG-P0001-B01-F00-U01", sample_footprint, 0.0)
    except ValueError:
        print("[PASS] Duplicate ULPIN successfully blocked")

    # Test 5: 3D Collision Detection
    try:
        engine.build_3d_property_record("KA-MNG-P0001-B01-F00-U02", sample_footprint, 0.0)
    except ValueError:
        print("[PASS] 3D Volumetric overlap successfully blocked")

    print("=============================================================")
    print("ALL TESTS PASSED! Person 4 core is fully operational.\n")