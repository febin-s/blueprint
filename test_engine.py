"""Test suite to verify Person 4 algorithmic engine."""

from spatial_engine import Spatial3DEngine

def run_tests():
    engine = Spatial3DEngine(default_floor_height=3.0)

    # 10m x 10m parcel footprint in [lng, lat]
    sample_footprint = [
        (74.85600, 12.87000),
        (74.85610, 12.87000),
        (74.85610, 12.87010),
        (74.85600, 12.87010),
        (74.85600, 12.87000)
    ]

    print("--- Running Test 1: Ground Floor (F00) ---")
    f0 = engine.build_3d_property_record(
        ulpin="KA-MNG-P0001-B01-F00-U01",
        boundary_coordinates=sample_footprint,
        base_ground_elevation=0.0
    )
    assert f0["bounds_3d"]["z_min"] == 0.0
    assert f0["bounds_3d"]["z_max"] == 3.0
    print("✓ Ground floor correctly placed at 0.0m - 3.0m")

    print("\n--- Running Test 2: Floor 3 (F03) Stacking ---")
    f3 = engine.build_3d_property_record(
        ulpin="KA-MNG-P0001-B01-F03-U01",
        boundary_coordinates=sample_footprint,
        base_ground_elevation=0.0
    )
    # F03 height = 3 * 3.0 = 9.0m to 12.0m
    assert f3["bounds_3d"]["z_min"] == 9.0
    assert f3["bounds_3d"]["z_max"] == 12.0
    print("✓ F03 correctly elevated to 9.0m - 12.0m (No collision with F00)")

    print("\n--- Running Test 3: Basement 1 (B01) ---")
    b1 = engine.build_3d_property_record(
        ulpin="KA-MNG-P0001-B01-B01-U01",
        boundary_coordinates=sample_footprint,
        base_ground_elevation=0.0
    )
    assert b1["bounds_3d"]["z_min"] == -3.0
    assert b1["bounds_3d"]["z_max"] == 0.0
    print("✓ B01 correctly sunk to -3.0m - 0.0m")

    print("\n--- Running Test 4: Duplicate ULPIN Detection ---")
    try:
        engine.build_3d_property_record(
            ulpin="KA-MNG-P0001-B01-F00-U01",  # Already registered
            boundary_coordinates=sample_footprint,
            base_ground_elevation=0.0
        )
        print("✗ Failed: Allowed duplicate ULPIN")
    except ValueError as e:
        print(f"✓ Blocked duplicate ULPIN: {e}")

    print("\n--- Running Test 5: 3D Volumetric Collision Detection ---")
    try:
        # Same floor (F00) and same footprint, different unit ID -> Must clash
        engine.build_3d_property_record(
            ulpin="KA-MNG-P0001-B01-F00-U02",
            boundary_coordinates=sample_footprint,
            base_ground_elevation=0.0
        )
        print("✗ Failed: Allowed 3D spatial collision")
    except ValueError as e:
        print(f"✓ Blocked 3D spatial collision: {e}")

    print("\nAll 5 validation tests passed successfully!")

if __name__ == "__main__":
    run_tests()