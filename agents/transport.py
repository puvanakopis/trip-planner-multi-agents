from typing import Dict, Any, List
from services.mcp_client import MCPClient

class TransportAgent:
    @staticmethod
    async def process(origin: str, destinations: List[str]) -> List[Dict[str, Any]]:
        routes = []
        stops = [origin] + destinations + [origin]
        for i in range(len(stops) - 1):
            r = await MCPClient.get_route(stops[i], stops[i+1])
            routes.append(r)
        return routes
