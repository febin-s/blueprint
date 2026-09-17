from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "property.db")


def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    db.execute("""
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
        )
    """)
    db.commit()

    count = db.execute("SELECT COUNT(*) AS c FROM properties").fetchone()["c"]
    if count == 0:
        seed = [
            ("IN-KA-MNG-2026-000421", "Rajesh Kumar", "Residential",
             "Ocean View Residency", "Mangaluru, Karnataka", 5, "5B"),
            ("IN-KA-MNG-2026-000420", "Priya Sharma", "Residential",
             "Ocean View Residency", "Mangaluru, Karnataka", 3, "3A"),
            ("IN-KA-UDP-2026-000419", "Anil Thomas", "Commercial",
             "Green Acres Tower", "Udupi, Karnataka", 1, "102")
        ]
        for row in seed:
            db.execute("""
                INSERT INTO properties
                (ulpin, owner, property_type, building_name, address,
                 floor_number, unit_number, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (*row, datetime.utcnow().isoformat()))
        db.commit()
    db.close()


def property_dict(row):
    return {
        "id": row["id"],
        "ulpin": row["ulpin"],
        "owner": row["owner"],
        "property_type": row["property_type"],
        "building_name": row["building_name"],
        "address": row["address"],
        "floor_number": row["floor_number"],
        "unit_number": row["unit_number"],
        "created_at": row["created_at"]
    }


def generate_ulpin(address):
    year = datetime.now().year
    district = "MNG"
    address_upper = address.upper()
    if "UDUPI" in address_upper:
        district = "UDP"
    elif "BENGALURU" in address_upper or "BANGALORE" in address_upper:
        district = "BLR"
    elif "BELAGAVI" in address_upper:
        district = "BLG"

    while True:
        number = random.randint(100000, 999999)
        ulpin = f"IN-KA-{district}-{year}-{number}"
        db = get_db()
        exists = db.execute(
            "SELECT 1 FROM properties WHERE ulpin = ?", (ulpin,)
        ).fetchone()
        db.close()
        if not exists:
            return ulpin


@app.get("/")
def home():
    return jsonify({
        "name": "3D ULPIN Property Mapping API",
        "status": "running"
    })


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/properties")
def get_properties():
    db = get_db()
    rows = db.execute(
        "SELECT * FROM properties ORDER BY id DESC"
    ).fetchall()
    db.close()
    return jsonify([property_dict(row) for row in rows])


@app.get("/api/properties/<int:property_id>")
def get_property(property_id):
    db = get_db()
    row = db.execute(
        "SELECT * FROM properties WHERE id = ?", (property_id,)
    ).fetchone()
    db.close()

    if not row:
        return jsonify({"error": "Property not found"}), 404
    return jsonify(property_dict(row))


@app.get("/api/properties/search")
def search_properties():
    q = request.args.get("q", "").strip()

    if not q:
        return get_properties()

    like = f"%{q}%"
    db = get_db()
    rows = db.execute("""
        SELECT * FROM properties
        WHERE ulpin LIKE ?
           OR owner LIKE ?
           OR building_name LIKE ?
           OR address LIKE ?
           OR unit_number LIKE ?
           OR property_type LIKE ?
        ORDER BY id DESC
    """, (like, like, like, like, like, like)).fetchall()
    db.close()

    return jsonify([property_dict(row) for row in rows])


@app.post("/api/properties")
def create_property():
    data = request.get_json(silent=True) or {}

    required = [
        "owner", "property_type", "building_name",
        "address", "floor_number", "unit_number"
    ]

    missing = [field for field in required if data.get(field) in (None, "")]
    if missing:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing
        }), 400

    try:
        floor_number = int(data["floor_number"])
        if floor_number < 0:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({"error": "floor_number must be a non-negative integer"}), 400

    ulpin = data.get("ulpin") or generate_ulpin(data["address"])

    db = get_db()
    try:
        cursor = db.execute("""
            INSERT INTO properties
            (ulpin, owner, property_type, building_name, address,
             floor_number, unit_number, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ulpin,
            str(data["owner"]).strip(),
            str(data["property_type"]).strip(),
            str(data["building_name"]).strip(),
            str(data["address"]).strip(),
            floor_number,
            str(data["unit_number"]).strip(),
            datetime.utcnow().isoformat()
        ))
        db.commit()
        row = db.execute(
            "SELECT * FROM properties WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
        return jsonify(property_dict(row)), 201
    except sqlite3.IntegrityError:
        db.rollback()
        return jsonify({"error": "ULPIN already exists"}), 409
    finally:
        db.close()


@app.put("/api/properties/<int:property_id>")
def update_property(property_id):
    data = request.get_json(silent=True) or {}

    db = get_db()
    old = db.execute(
        "SELECT * FROM properties WHERE id = ?", (property_id,)
    ).fetchone()

    if not old:
        db.close()
        return jsonify({"error": "Property not found"}), 404

    fields = [
        "owner", "property_type", "building_name",
        "address", "floor_number", "unit_number"
    ]

    values = {field: data.get(field, old[field]) for field in fields}

    try:
        values["floor_number"] = int(values["floor_number"])
        if values["floor_number"] < 0:
            raise ValueError
    except (TypeError, ValueError):
        db.close()
        return jsonify({"error": "floor_number must be a non-negative integer"}), 400

    db.execute("""
        UPDATE properties
        SET owner = ?, property_type = ?, building_name = ?,
            address = ?, floor_number = ?, unit_number = ?
        WHERE id = ?
    """, (
        str(values["owner"]).strip(),
        str(values["property_type"]).strip(),
        str(values["building_name"]).strip(),
        str(values["address"]).strip(),
        values["floor_number"],
        str(values["unit_number"]).strip(),
        property_id
    ))
    db.commit()

    row = db.execute(
        "SELECT * FROM properties WHERE id = ?", (property_id,)
    ).fetchone()
    db.close()
    return jsonify(property_dict(row))


@app.delete("/api/properties/<int:property_id>")
def delete_property(property_id):
    db = get_db()
    cursor = db.execute(
        "DELETE FROM properties WHERE id = ?", (property_id,)
    )
    db.commit()
    db.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Property not found"}), 404

    return jsonify({"message": "Property deleted"})


@app.get("/api/stats")
def stats():
    db = get_db()
    total = db.execute(
        "SELECT COUNT(*) AS c FROM properties"
    ).fetchone()["c"]
    mapped = db.execute("""
        SELECT COUNT(*) AS c FROM properties
        WHERE floor_number IS NOT NULL AND unit_number != ''
    """).fetchone()["c"]
    db.close()

    return jsonify({
        "registered_properties": total,
        "vertically_mapped_units": mapped,
        "ulpins_generated": total
    })


@app.get("/api/buildings")
def buildings():
    db = get_db()
    rows = db.execute("""
        SELECT building_name, address,
               COUNT(*) AS units,
               COUNT(DISTINCT floor_number) AS floors
        FROM properties
        GROUP BY building_name, address
        ORDER BY building_name
    """).fetchall()
    db.close()

    return jsonify([{
        "building_name": r["building_name"],
        "address": r["address"],
        "units": r["units"],
        "floors": r["floors"]
    } for r in rows])


@app.get("/api/buildings/<path:building_name>")
def building_details(building_name):
    db = get_db()
    rows = db.execute("""
        SELECT * FROM properties
        WHERE building_name = ?
        ORDER BY floor_number DESC, unit_number
    """, (building_name,)).fetchall()
    db.close()

    return jsonify([property_dict(row) for row in rows])


@app.get("/api/reports")
def reports():
    db = get_db()
    by_type = db.execute("""
        SELECT property_type, COUNT(*) AS count
        FROM properties
        GROUP BY property_type
    """).fetchall()
    by_building = db.execute("""
        SELECT building_name, COUNT(*) AS count
        FROM properties
        GROUP BY building_name
        ORDER BY count DESC
    """).fetchall()
    db.close()

    return jsonify({
        "by_property_type": [
            {"property_type": r["property_type"], "count": r["count"]}
            for r in by_type
        ],
        "by_building": [
            {"building_name": r["building_name"], "count": r["count"]}
            for r in by_building
        ]
    })


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
