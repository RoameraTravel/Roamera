from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests

# --- Replace with your actual API key (avoid hardcoding in production) ---
API_KEY = "8B48FA4FCDE043B4984FB2B1BC239C7F"

# Input schema
class TripAdvisorToolInput(BaseModel):
    search_query: str = Field(..., description="The destination or place to search on TripAdvisor")

# Tool class
class TripAdvisorSearchTool(BaseTool):
    name: str = "TripAdvisor Search Tool"
    description: str = (
        "Useful for retrieving destination or location details from TripAdvisor based on a user search query."
    )
    args_schema: Type[BaseModel] = TripAdvisorToolInput

    def _run(self, search_query: str) -> str:
        url = "https://api.content.tripadvisor.com/api/v1/location/search"
        params = {
            "key": API_KEY,
            "language": "en",
            "searchQuery": search_query
        }
        headers = {
            "accept": "application/json"
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            if "data" in data:
                results = data["data"]
                if not results:
                    return "No results found for the given search."

                return "\n".join(
                    f"{place.get('name', 'Unknown')} - {place.get('address_obj', {}).get('address_string', 'No address')}"
                    for place in results[:5]
                )
            else:
                return f"Unexpected response: {data}"
        except Exception as e:
            return f"Error fetching data from TripAdvisor: {str(e)}"
