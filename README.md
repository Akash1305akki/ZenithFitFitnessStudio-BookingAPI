# 🧘‍♂️ ZenithFit Fitness Studio - Booking API

A simple backend API for managing class bookings at a fictional ZenithFit Fitness Studio. Built using FastAPI and SQLite.

---

## 🚀 Features

- View upcoming classes (`/classes`)
- Book a slot in a class (`/book`)
- View all bookings by email (`/bookings`)
- Handles timezone conversion from IST
- Input validation and error handling

---

## 📦 Tech Stack

- Python 3.9+
- FastAPI
- SQLite (in-memory/local)
- Pydantic
- Uvicorn
- pytz

---

## 🧪 API Endpoints

### ✅ GET `/classes`

Query Params:

- `timezone` (optional): Target timezone (default = `Asia/Kolkata`)

Response:

```json
[
  {
    "id": 1,
    "name": "Yoga",
    "datetime": "2025-07-04T09:00:00+05:30",
    "instructor": "Rina",
    "slots": 5
  }
]
```
