from pydantic import BaseModel, Field
from typing import Optional, List

class LocationCoordinates(BaseModel):
    latitude: float
    longitude: float

class DestinationInfo(BaseModel):
    name: str
    is_valid_sri_lanka: bool = True
    display_name: Optional[str] = None
    province: Optional[str] = None
    district: Optional[str] = None
    coordinates: Optional[LocationCoordinates] = None
    description: Optional[str] = None
    highlights: List[str] = Field(default_factory=list)
    nearby_places: List[str] = Field(default_factory=list)
    source: str = "OpenStreetMap / Nominatim"
    retrieved_at: Optional[str] = None
    status: str = "online"
