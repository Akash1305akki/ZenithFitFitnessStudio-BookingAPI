# booking_api/main.py
from fastapi import FastAPI, HTTPException, Query, Path
from typing import List, Optional
from db import init_db, get_db
from models import (
    create_tables, get_all_classes, book_class, get_bookings_by_email,
    create_class, update_class, delete_class, get_class_by_id,
    get_available_classes, get_all_bookings, get_summary
)
from schemas import (
    BookingRequest, BookingResponse, ClassResponse, 
    ClassCreateRequest, ClassUpdateRequest, ClassSummary
)
from utils import convert_class_times
import logging

app = FastAPI(title="ZenithFit Fitness Studio - Booking API")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("startup")
def startup():
    """Initialize database on startup."""
    init_db()
    create_tables()

@app.get("/classes", response_model=List[ClassResponse], tags=["Available API Services"])
def read_classes(timezone: str = Query("Asia/Kolkata", description="Timezone to convert class times")):
    """Fetch all classes with times adjusted to the provided timezone."""
    with get_db() as db:
        classes = get_all_classes(db)
        return convert_class_times(classes, timezone)

@app.post("/book", response_model=BookingResponse, tags=["Available API Services"])
def create_booking(booking: BookingRequest):
    """Book a slot in a class if available."""
    with get_db() as db:
        try:
            return book_class(db, booking)
        except ValueError as e:
            logger.error(f"Booking failed: {e}")
            raise HTTPException(status_code=400, detail=str(e))

@app.get("/bookings", response_model=List[BookingResponse], tags=["Available API Services"])
def get_bookings(email: str = Query(..., description="Client email to fetch bookings")):
    """Retrieve all bookings for a given email."""
    with get_db() as db:
        return get_bookings_by_email(db, email)

@app.post("/create-class", response_model=ClassResponse, tags=["Available API Services"])
def create_new_class(class_data: ClassCreateRequest):
    """Create a new fitness class (admin only)."""
    with get_db() as db:
        return create_class(db, class_data)

@app.put("/update-class/{class_id}", response_model=ClassResponse, tags=["Available API Services"])
def update_existing_class(
    class_id: int = Path(..., description="ID of the class to update"),
    class_data: ClassUpdateRequest = ...
):
    """Update an existing class's details."""
    with get_db() as db:
        try:
            return update_class(db, class_id, class_data)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

@app.delete("/class/{class_id}", tags=["Available API Services"])
def remove_class(class_id: int = Path(..., description="ID of the class to delete")):
    """Delete a class and optionally its bookings."""
    with get_db() as db:
        deleted = delete_class(db, class_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Class not found")
        return {"message": "Class deleted successfully"}

@app.get("/class/{class_id}", response_model=ClassResponse, tags=["Available API Services"])
def get_class_detail(class_id: int):
    """Get detailed information for a specific class."""
    with get_db() as db:
        result = get_class_by_id(db, class_id)
        if not result:
            raise HTTPException(status_code=404, detail="Class not found")
        return result

@app.get("/classes/available", response_model=List[ClassResponse], tags=["Available API Services"])
def get_only_available_classes():
    """Return all future classes that still have available slots."""
    with get_db() as db:
        return get_available_classes(db)

@app.get("/bookings/all", response_model=List[BookingResponse], tags=["Available API Services"])
def get_all_bookings_admin():
    """Return all bookings (admin use)."""
    with get_db() as db:
        return get_all_bookings(db)

@app.get("/analytics/summary", response_model=ClassSummary, tags=["Available API Services"])
def get_summary_analytics():
    """Return a summary of total bookings, top class, and more."""
    with get_db() as db:
        return get_summary(db)
