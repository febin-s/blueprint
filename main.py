# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Tuple
from spatial_engine import Spatial3DEngine

app = FastAPI(title="Person 4 3D-ULPIN Engine")
engine = Spatial3DEngine(default_floor_height=3.0)

class ParcelInput(BaseModel):
    ulpin: str
    coords: List[Tuple[float, float]]
    ground_elevation: float = 0.0

@app.post("/calculate-3d")
def calculate(data: ParcelInput):
    try:
        result = engine.build_3d_property_record(
            ulpin=data.ulpin,
            boundary_coordinates=data.coords,
            base_ground_elevation=data.ground_elevation
        )
        return {"status": "SUCCESS", "data": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))