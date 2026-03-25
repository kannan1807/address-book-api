# Address Book API

A RESTful API built with FastAPI that allows you to create, update, delete,
and search addresses by GPS proximity.

---

## Requirements

- Python 3.11+
- pip

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/address-book-api.git
cd address-book-api
```

### 2. Create and activate virtual environment
```bash
# Windows
py -3.11 -m venv venv
venv\Scripts\activate

# macOS / Linux
python3.11 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create environment file
```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

### 5. Run the application
```bash
uvicorn app.main:app --reload
```

### 6. Open Swagger UI
```
http://127.0.0.1:8000/docs
```

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /addresses/ | Create a new address |
| GET | /addresses/ | List all addresses |
| GET | /addresses/{id} | Get address by ID |
| PATCH | /addresses/{id} | Partially update an address |
| DELETE | /addresses/{id} | Delete an address |
| GET | /addresses/nearby/search | Find addresses within a radius |

---

## Proximity Search Example

Find all addresses within 10km of Chennai, India:
```
GET /addresses/nearby/search?latitude=13.0827&longitude=80.2707&distance_km=10
```

---

## Sample Request — Create Address
```json
POST /addresses/
{
  "name": "Marina Beach",
  "street": "Kamarajar Salai",
  "city": "Chennai",
  "country": "India",
  "latitude": 13.0500,
  "longitude": 80.2824
}
```

---

## Project Structure
```
address_book/
├── app/
│   ├── main.py         — FastAPI entry point
│   ├── config.py       — Settings and environment variables
│   ├── database.py     — SQLite + SQLAlchemy setup
│   ├── models.py       — ORM models
│   ├── schemas.py      — Pydantic validation schemas
│   ├── crud.py         — Database operations
│   ├── utils.py        — Geodesic distance helper
│   └── routers/
│       └── addresses.py — Route handlers
├── logs/               — Auto-created log files
├── requirements.txt
├── .env
└── README.md
```

---

## Logs

All API events are logged to both the terminal and `logs/app.log`.
Log files rotate automatically at 5MB, keeping the last 3 files.