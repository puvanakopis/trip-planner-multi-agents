from typing import Dict, Any, List
from services.mcp_client import MCPClient

class ActivityAgent:
    @staticmethod
    async def process(destinations: List[str]) -> List[Dict[str, Any]]:
        all_activities = []
        for dest in destinations:
            acts = await MCPClient.get_activities(dest)
            all_activities.extend(acts)
        return all_activities
