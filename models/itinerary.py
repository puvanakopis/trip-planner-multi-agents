from pydantic import BaseModel, Field
from typing import Optional, List

class ActivitySlot(BaseModel):
    time_of_day: str  # "Morning", "Afternoon", "Evening"
    title: str
    description: str
    location: str
    estimated_cost: float = 0.0
    cost_currency: str = "LKR"
    cost_status: str = "estimated"

class DayPlan(BaseModel):
    day_number: int
    destination: str
    title: str
    summary: str
    morning: ActivitySlot
    afternoon: ActivitySlot
    evening: ActivitySlot
    accommodation: Optional[str] = None
    travel_segment: Optional[str] = None

class ItineraryPlan(BaseModel):
    title: str
    total_days: int
    days: List[DayPlan] = Field(default_factory=list)
    overall_summary: str
