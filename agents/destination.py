from typing import Dict, Any, List
from services.mcp_client import MCPClient

class DestinationAgent:
    @staticmethod
    async def process(destinations: List[str]) -> List[Dict[str, Any]]:
        results = []
        for dest in destinations:
            details = await MCPClient.get_destination_details(dest)
            results.append(details)
        return results
