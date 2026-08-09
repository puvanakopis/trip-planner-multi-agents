from pydantic import BaseModel, Field
from typing import Optional

class HotelOption(BaseModel):
    name: str
    destination: str
    price_per_night: Optional[float] = None
    currency: str = "LKR"
    rating: Optional[float] = None
    address: Optional[str] = None
    amenities: list[str] = Field(default_factory=list)
    booking_url: Optional[str] = None
    source: str = "External hotel provider"
    retrieved_at: Optional[str] = None
    status: str = "online"  # "online" or "unavailable"
    note: Optional[str] = None
