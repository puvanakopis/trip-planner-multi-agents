from typing import Dict, Any, List
from models.itinerary import ItineraryPlan, DayPlan, ActivitySlot

class ItineraryAgent:
    @staticmethod
    async def process(destinations: List[str], duration_days: int, activities: List[Dict[str, Any]], origin: str) -> Dict[str, Any]:
        days = []
        num_dests = len(destinations) if destinations else 1

        for d in range(1, duration_days + 1):
            dest_index = (d - 1) % num_dests
            current_dest = destinations[dest_index] if destinations else "Sri Lanka"
            
            # Select activities for destination
            dest_acts = [a for a in activities if a.get("destination") == current_dest]
            act1 = dest_acts[0] if len(dest_acts) > 0 else {"title": f"Explore {current_dest}", "estimated_cost": 0.0}
            act2 = dest_acts[1] if len(dest_acts) > 1 else {"title": f"Visit Scenic Spot in {current_dest}", "estimated_cost": 500.0}
            act3 = dest_acts[2] if len(dest_acts) > 2 else {"title": f"Relax & Dinner in {current_dest}", "estimated_cost": 1500.0}

            travel_seg = f"{origin} to {current_dest}" if d == 1 else f"{destinations[(dest_index-1)%num_dests]} to {current_dest}" if (d-1)%num_dests != dest_index else None

            days.append({
                "day_number": d,
                "destination": current_dest,
                "title": f"Day {d}: Experience {current_dest}",
                "summary": f"Full day exploring attractions, culture, and nature around {current_dest}.",
                "morning": {
                    "time_of_day": "Morning",
                    "title": act1.get("title"),
                    "description": f"Morning session: {act1.get('title')}",
                    "location": current_dest,
                    "estimated_cost": act1.get("estimated_cost", 0.0)
                },
                "afternoon": {
                    "time_of_day": "Afternoon",
                    "title": act2.get("title"),
                    "description": f"Afternoon exploration: {act2.get('title')}",
                    "location": current_dest,
                    "estimated_cost": act2.get("estimated_cost", 0.0)
                },
                "evening": {
                    "time_of_day": "Evening",
                    "title": act3.get("title"),
                    "description": f"Evening relaxation: {act3.get('title')}",
                    "location": current_dest,
                    "estimated_cost": act3.get("estimated_cost", 0.0)
                },
                "accommodation": f"Hotel in {current_dest}",
                "travel_segment": travel_seg
            })

        return {
            "title": f"{duration_days}-Day Sri Lanka Travel Itinerary",
            "total_days": duration_days,
            "days": days,
            "overall_summary": f"Complete multi-day operational itinerary covering {', '.join(destinations)} starting from {origin}."
        }
