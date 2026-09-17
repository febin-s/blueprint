# 3D ULPIN Property Mapping - Backend

This backend is designed for the `frontend/index.html` in the Blueprint repository.

## Stack

- Python
- Flask
- SQLite
- Flask-CORS

## 1. Install

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

Then:

```bash
pip install -r requirements.txt
```

## 2. Start the API

```bash
python app.py
```

The API will run at:

```text
http://127.0.0.1:5000
```

Health check:

```text
http://127.0.0.1:5000/api/health
```

A `property.db` file is created automatically.

## Main API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/properties` | All properties |
| GET | `/api/properties/<id>` | One property |
| GET | `/api/properties/search?q=Rajesh` | Search |
| POST | `/api/properties` | Register property |
| PUT | `/api/properties/<id>` | Update property |
| DELETE | `/api/properties/<id>` | Delete property |
| GET | `/api/stats` | Dashboard statistics |
| GET | `/api/buildings` | Building summary |
| GET | `/api/buildings/<building_name>` | Building properties |
| GET | `/api/reports` | Report data |

## Example POST body

```json
{
  "owner": "Meera Nair",
  "property_type": "Residential",
  "building_name": "Ocean View Residency",
  "address": "Mangaluru, Karnataka",
  "floor_number": 5,
  "unit_number": "5B"
}
```

The backend generates the ULPIN automatically if one is not supplied.

## Connecting your GitHub Pages frontend

Your GitHub Pages frontend cannot execute Python itself. Host this Flask API separately, then set the API URL in your frontend JavaScript.

Example:

```js
const API = "https://YOUR-BACKEND-DOMAIN.com";
```

Register:

```js
const response = await fetch(`${API}/api/properties`, {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify({
    owner,
    property_type,
    building_name,
    address,
    floor_number,
    unit_number
  })
});
```

Load properties:

```js
const response = await fetch(`${API}/api/properties`);
const properties = await response.json();
```

Search:

```js
const response = await fetch(
  `${API}/api/properties/search?q=${encodeURIComponent(query)}`
);
const results = await response.json();
```

## Deployment note

SQLite is suitable for development and simple deployments. For a production multi-user application, use PostgreSQL or another persistent database.

Deploy the Flask API on a Python-capable host and put its HTTPS URL into the frontend.

Do not put database passwords, API keys, or other secrets inside `index.html`.
