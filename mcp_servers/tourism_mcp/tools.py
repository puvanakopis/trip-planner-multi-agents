from mcp_servers.tourism_mcp.providers.nominatim import TourismProvider

tools = [
    TourismProvider.validate_location,
    TourismProvider.get_destination_details
]
