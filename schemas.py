from pydantic import BaseModel, EmailStr
from typing import Optional


class ClassResponse(BaseModel):
    id: int
    name: str
    datetime: str  # ISO format string (to be converted by timezone logic)
    instructor: str
    slots: int

    class Config:
        from_attributes = True


class BookingRequest(BaseModel):
    class_id: int
    client_name: str
    client_email: EmailStr


class BookingResponse(BaseModel):
    class_id: int
    client_name: str
    client_email: EmailStr


class ClassCreateRequest(BaseModel):
    name: str
    datetime: str  # ISO format expected: e.g., '2025-07-06T08:00:00'
    instructor: str
    slots: int


class ClassUpdateRequest(BaseModel):
    name: str
    datetime: str  # ISO format expected
    instructor: str
    slots: int


class ClassSummary(BaseModel):
    total_classes: int
    total_bookings: int
    top_class: Optional[str] = None
