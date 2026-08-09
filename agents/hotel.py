from typing import Dict, Any, List
from services.mcp_client import MCPClient

class HotelAgent:
    @staticmethod
    async def process(destinations: List[str], budget: float) -> List[Dict[str, Any]]:
        results = []
        for dest in destinations:
            res = await MCPClient.search_hotels(dest, budget)
            results.append(res)
        return results
