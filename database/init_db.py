from .database import engine, Base
from . import models

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")