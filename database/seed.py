from .database import SessionLocal
from .models import Property, Building, Floor, Unit


def seed_database():
    db = SessionLocal()

    try:
        # Check if data already exists
        existing_property = db.query(Property).first()

        if existing_property:
            print("Demo data already exists.")
            return

        # -------------------------
        # 1. PROPERTY
        # -------------------------
        property1 = Property(
            property_code="PROP001",
            owner_name="Demo Owner",
            address="Kochi, Kerala",
            latitude=9.9312,
            longitude=76.2673
        )

        db.add(property1)
        db.flush()

        # -------------------------
        # 2. BUILDING
        # -------------------------
        building1 = Building(
            property_id=property1.id,
            building_name="Building A",
            building_number="A01",
            total_floors=3,
            basement_levels=1,
            building_height=12.0
        )

        db.add(building1)
        db.flush()

        # -------------------------
        # 3. BASEMENT FLOOR
        # -------------------------
        basement = Floor(
            building_id=building1.id,
            floor_number=-1,
            floor_name="Basement 1",
            floor_height=3.0,
            vertical_position=-3.0
        )

        db.add(basement)

        # -------------------------
        # 4. GROUND FLOOR
        # -------------------------
        ground = Floor(
            building_id=building1.id,
            floor_number=0,
            floor_name="Ground Floor",
            floor_height=3.0,
            vertical_position=0.0
        )

        db.add(ground)
        db.flush()

        # -------------------------
        # 5. UNITS ON GROUND FLOOR
        # -------------------------
        unit1 = Unit(
            floor_id=ground.id,
            unit_number="G01",
            unit_type="Flat",
            area=85.5,
            ulpin="ULPIN-DEMO-000001",
            latitude=9.9312,
            longitude=76.2673,
            vertical_position=1.5
        )

        unit2 = Unit(
            floor_id=ground.id,
            unit_number="G02",
            unit_type="Flat",
            area=90.0,
            ulpin="ULPIN-DEMO-000002",
            latitude=9.9312,
            longitude=76.2673,
            vertical_position=1.5
        )

        db.add_all([unit1, unit2])

        # -------------------------
        # 6. FIRST FLOOR
        # -------------------------
        first = Floor(
            building_id=building1.id,
            floor_number=1,
            floor_name="First Floor",
            floor_height=3.0,
            vertical_position=3.0
        )

        db.add(first)
        db.flush()

        # -------------------------
        # 7. UNITS ON FIRST FLOOR
        # -------------------------
        unit3 = Unit(
            floor_id=first.id,
            unit_number="101",
            unit_type="Flat",
            area=85.5,
            ulpin="ULPIN-DEMO-000101",
            latitude=9.9312,
            longitude=76.2673,
            vertical_position=4.5
        )

        unit4 = Unit(
            floor_id=first.id,
            unit_number="102",
            unit_type="Flat",
            area=90.0,
            ulpin="ULPIN-DEMO-000102",
            latitude=9.9312,
            longitude=76.2673,
            vertical_position=4.5
        )

        db.add_all([unit3, unit4])

        # -------------------------
        # 8. SECOND FLOOR
        # -------------------------
        second = Floor(
            building_id=building1.id,
            floor_number=2,
            floor_name="Second Floor",
            floor_height=3.0,
            vertical_position=6.0
        )

        db.add(second)
        db.flush()

        unit5 = Unit(
            floor_id=second.id,
            unit_number="201",
            unit_type="Flat",
            area=85.5,
            ulpin="ULPIN-DEMO-000201",
            latitude=9.9312,
            longitude=76.2673,
            vertical_position=7.5
        )

        unit6 = Unit(
            floor_id=second.id,
            unit_number="202",
            unit_type="Flat",
            area=90.0,
            ulpin="ULPIN-DEMO-000202",
            latitude=9.9312,
            longitude=76.2673,
            vertical_position=7.5
        )

        db.add_all([unit5, unit6])

        # Save everything
        db.commit()

        print("Demo data inserted successfully!")

    except Exception as e:
        db.rollback()
        print("Error:", e)

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
    