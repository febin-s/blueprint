from app import models


def unit_to_dict(unit):

    return {
        "unitId": unit.id,
        "unitNumber": unit.unit_number,
        "unitType": unit.unit_type,
        "areaSqft": unit.area_sqft,
        "ownerName": unit.owner_name,
        "status": unit.status
    }


def floor_to_dict(floor):

    return {
        "floorId": floor.id,
        "floorNumber": floor.floor_number,
        "name": floor.name,
        "height": floor.height,
        "units": [
            unit_to_dict(unit)
            for unit in floor.units
        ]
    }


def building_to_dict(building):

    return {
        "buildingId": building.id,
        "name": building.name,
        "buildingType": building.building_type,
        "address": building.address,
        "latitude": building.latitude,
        "longitude": building.longitude,
        "height": building.height,
        "floors": [
            floor_to_dict(floor)
            for floor in sorted(
                building.floors,
                key=lambda x: x.floor_number
            )
        ]
    }


def property_to_dict(property_data):

    buildings = sorted(
        property_data.buildings,
        key=lambda x: x.id
    )

    floors = []
    units = []

    for building in buildings:

        for floor in building.floors:

            floors.append(
                floor_to_dict(floor)
            )

            for unit in floor.units:

                units.append(
                    unit_to_dict(unit)
                )

    return {
        "propertyId": property_data.id,
        "ulpin": property_data.ulpin,
        "state": property_data.state,
        "district": property_data.district,
        "location": property_data.location,

        "building": [
            building_to_dict(building)
            for building in buildings
        ],

        "floors": floors,
        "units": units
    }