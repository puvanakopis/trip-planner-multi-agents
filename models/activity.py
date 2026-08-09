from pydantic import BaseModel, Field
from typing import Optional, List

class ActivityItem(BaseModel):
    title: str
    destination: str
    category: str  # "Nature", "Culture", "Adventure", "Beach", "Wildlife", "Hiking", "Historical", "Food"
    description: Optional[str] = None
    estimated_cost: float = 0.0
    currency: str = "LKR"
    duration_hours: Optional[float] = 2.0
    source: str = "OpenStreetMap / Overpass / Wikidata"
    retrieved_at: Optional[str] = None
    status: str = "online"
