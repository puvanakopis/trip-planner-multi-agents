from pydantic import BaseModel, Field
from typing import Optional, List

class DailyForecast(BaseModel):
    date: str
    temperature_max: float
    temperature_min: float
    rain_probability: int
    condition: str

class WeatherInfo(BaseModel):
    destination: str
    temperature_celsius: Optional[float] = None
    rain_probability: Optional[int] = None
    condition: str = "Unknown"
    forecast: List[DailyForecast] = Field(default_factory=list)
    source: str = "Open-Meteo API"
    retrieved_at: Optional[str] = None
    status: str = "online"
