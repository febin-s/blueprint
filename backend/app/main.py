from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.properties import router as properties_router
from app.routes.buildings import router as buildings_router
from app.routes.floors import router as floors_router
from app.routes.units import router as units_router
from app.routes.three_d import router as three_d_router

app = FastAPI(
    title="3D ULPIN Property Mapping API",
    description="SIH26011 Backend API",
    version="1.0.0"
)


# --------------------------------
# CORS
# --------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(properties_router)
app.include_router(buildings_router)
app.include_router(floors_router)
app.include_router(units_router)
app.include_router(three_d_router)

# --------------------------------
# ROOT
# --------------------------------

@app.get("/")
def home():
    return {
        "message": "3D ULPIN Property Mapping API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }


# --------------------------------
# HEALTH CHECK
# --------------------------------

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "ULPIN Backend API"
    }