CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ulpin TEXT UNIQUE NOT NULL,
    owner TEXT NOT NULL,
    property_type TEXT NOT NULL,
    building_name TEXT NOT NULL,
    address TEXT NOT NULL,
    floor_number INTEGER NOT NULL,
    unit_number TEXT NOT NULL,
    created_at TEXT NOT NULL
);