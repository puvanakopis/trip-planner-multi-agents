from typing import Dict, Any, List

class ValidatorAgent:
    @staticmethod
    async def process(state: Dict[str, Any]) -> Dict[str, Any]:
        """Validates itinerary feasibility, logical flow, and budget parameters."""
        budget_info = state.get("budget", {})
        itinerary = state.get("itinerary", {})
        is_sri_lanka = state.get("travel_request", {}).get("is_sri_lanka", True)

        validation_issues = []
        
        if not is_sri_lanka:
            validation_issues.append("Requested destinations are outside Sri Lanka.")

        if budget_info and not budget_info.get("is_within_budget", True):
            diff = abs(budget_info.get("remaining_budget", 0))
            curr = budget_info.get("currency", "LKR")
            validation_issues.append(f"Estimated itinerary cost exceeds budget by {diff:.2f} {curr}.")

        days = itinerary.get("days", [])
        if not days:
            validation_issues.append("No itinerary days generated.")

        is_valid = len(validation_issues) == 0
        
        return {
            "is_valid": is_valid,
            "validation_issues": validation_issues,
            "status": "validated" if is_valid else "flagged"
        }
