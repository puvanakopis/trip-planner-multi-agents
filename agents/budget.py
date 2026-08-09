from typing import Dict, Any, List
from models.travel import BudgetBreakdown, CostItem

class BudgetAgent:
    @staticmethod
    async def process(total_budget: float, transport_routes: List[Dict[str, Any]], activities: List[Dict[str, Any]], duration_days: int) -> Dict[str, Any]:
        items = []
        cat_costs = {"Transport": 0.0, "Activities": 0.0, "Accommodation": 0.0, "Food & Miscellaneous": 0.0}

        # Transport costs
        for r in transport_routes:
            cost = r.get("estimated_cost_lkr", 0.0)
            orig = r.get("origin")
            dest = r.get("destination")
            items.append({
                "item": f"Transport: {orig} to {dest}",
                "cost": cost,
                "currency": "LKR",
                "source": r.get("source", "OSRM API"),
                "status": r.get("status", "estimated")
            })
            cat_costs["Transport"] += cost

        # Activity costs
        for a in activities:
            cost = a.get("estimated_cost", 0.0)
            items.append({
                "item": f"Activity: {a.get('title')}",
                "cost": cost,
                "currency": "LKR",
                "source": a.get("source", "Overpass API"),
                "status": a.get("status", "estimated")
            })
            cat_costs["Activities"] += cost

        # Accommodation estimation
        est_hotel_per_night = 12000.0
        hotel_total = est_hotel_per_night * max(1, duration_days - 1)
        items.append({
            "item": f"Estimated Accommodation ({duration_days - 1} nights)",
            "cost": hotel_total,
            "currency": "LKR",
            "source": "Sri Lanka Hotel Tariff DB",
            "status": "estimated"
        })
        cat_costs["Accommodation"] += hotel_total

        # Food estimation
        est_food_per_day = 4000.0 * duration_days
        items.append({
            "item": f"Estimated Food & Dining ({duration_days} days)",
            "cost": est_food_per_day,
            "currency": "LKR",
            "source": "Sri Lanka Tourism Board Standard",
            "status": "estimated"
        })
        cat_costs["Food & Miscellaneous"] += est_food_per_day

        total_est = sum(cat_costs.values())
        rem = total_budget - total_est

        return {
            "total_budget": total_budget,
            "currency": "LKR",
            "total_estimated_cost": total_est,
            "total_estimated_cost_lkr": total_est,
            "remaining_budget": rem,
            "is_within_budget": rem >= 0,
            "items": items,
            "categories": cat_costs
        }
