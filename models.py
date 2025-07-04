import sqlite3
from datetime import datetime
from schemas import (
    BookingRequest, BookingResponse, ClassResponse,
    ClassCreateRequest, ClassUpdateRequest, ClassSummary
)

def create_tables():
    """Create classes and bookings tables if they don't exist."""
    conn = sqlite3.connect("fitness.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            datetime TEXT NOT NULL,
            instructor TEXT NOT NULL,
            slots INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_id INTEGER NOT NULL,
            client_name TEXT NOT NULL,
            client_email TEXT NOT NULL,
            FOREIGN KEY (class_id) REFERENCES classes(id)
        )
    ''')

    conn.commit()
    conn.close()

def get_all_classes(db):
    """Fetch all upcoming classes from the DB."""
    cursor = db.cursor()
    cursor.execute("SELECT id, name, datetime, instructor, slots FROM classes")
    rows = cursor.fetchall()
    return [ClassResponse(id=row[0], name=row[1], datetime=row[2], instructor=row[3], slots=row[4]) for row in rows]

def get_class_by_id(db, class_id: int):
    """Get a specific class by ID."""
    cursor = db.cursor()
    cursor.execute("SELECT id, name, datetime, instructor, slots FROM classes WHERE id = ?", (class_id,))
    row = cursor.fetchone()
    if row:
        return ClassResponse(id=row[0], name=row[1], datetime=row[2], instructor=row[3], slots=row[4])
    return None

def get_available_classes(db):
    """Return classes that still have available slots."""
    cursor = db.cursor()
    cursor.execute("SELECT id, name, datetime, instructor, slots FROM classes WHERE slots > 0")
    rows = cursor.fetchall()
    return [ClassResponse(id=row[0], name=row[1], datetime=row[2], instructor=row[3], slots=row[4]) for row in rows]

def create_class(db, class_data: ClassCreateRequest):
    """Insert a new class into the DB."""
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO classes (name, datetime, instructor, slots) VALUES (?, ?, ?, ?)",
        (class_data.name, class_data.datetime, class_data.instructor, class_data.slots)
    )
    db.commit()
    class_id = cursor.lastrowid
    return get_class_by_id(db, class_id)

def update_class(db, class_id: int, class_data: ClassUpdateRequest):
    """Update existing class details."""
    cursor = db.cursor()
    cursor.execute("SELECT id FROM classes WHERE id = ?", (class_id,))
    if not cursor.fetchone():
        raise ValueError("Class not found")

    cursor.execute(
        "UPDATE classes SET name = ?, datetime = ?, instructor = ?, slots = ? WHERE id = ?",
        (class_data.name, class_data.datetime, class_data.instructor, class_data.slots, class_id)
    )
    db.commit()
    return get_class_by_id(db, class_id)

def delete_class(db, class_id: int):
    """Delete class by ID."""
    cursor = db.cursor()
    cursor.execute("DELETE FROM classes WHERE id = ?", (class_id,))
    db.commit()
    return cursor.rowcount > 0

def get_bookings_by_email(db, email: str):
    """Fetch all bookings for a specific email."""
    cursor = db.cursor()
    cursor.execute("SELECT class_id, client_name, client_email FROM bookings WHERE client_email = ?", (email,))
    rows = cursor.fetchall()
    return [BookingResponse(class_id=row[0], client_name=row[1], client_email=row[2]) for row in rows]

def get_all_bookings(db):
    """Return all bookings in DB."""
    cursor = db.cursor()
    cursor.execute("SELECT class_id, client_name, client_email FROM bookings")
    rows = cursor.fetchall()
    return [BookingResponse(class_id=row[0], client_name=row[1], client_email=row[2]) for row in rows]

def get_summary(db):
    """Return basic analytics summary."""
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM classes")
    total_classes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM bookings")
    total_bookings = cursor.fetchone()[0]

    cursor.execute('''
        SELECT classes.name, COUNT(bookings.id) as count
        FROM bookings
        JOIN classes ON classes.id = bookings.class_id
        GROUP BY class_id
        ORDER BY count DESC
        LIMIT 1
    ''')
    top_class_row = cursor.fetchone()
    top_class = top_class_row[0] if top_class_row else None

    return ClassSummary(
        total_classes=total_classes,
        total_bookings=total_bookings,
        top_class=top_class
    )

def book_class(db, booking: BookingRequest) -> BookingResponse:
    """Validate and book a class slot if available."""
    cursor = db.cursor()
    cursor.execute("SELECT slots FROM classes WHERE id = ?", (booking.class_id,))
    result = cursor.fetchone()
    if not result:
        raise ValueError("Class not found")

    available_slots = result[0]
    if available_slots <= 0:
        raise ValueError("No slots available")

    cursor.execute(
        "INSERT INTO bookings (class_id, client_name, client_email) VALUES (?, ?, ?)",
        (booking.class_id, booking.client_name, booking.client_email)
    )
    cursor.execute(
        "UPDATE classes SET slots = slots - 1 WHERE id = ?",
        (booking.class_id,)
    )
    db.commit()

    return BookingResponse(
        class_id=booking.class_id,
        client_name=booking.client_name,
        client_email=booking.client_email
    )
