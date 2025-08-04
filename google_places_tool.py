from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests

# Replace with your actual Google Places API key
API_KEY = "AIzaSyBPcU-aFgssg7jzuvuzCBUuNKlL2-EbsQo"

class GooglePlacesSearchInput(BaseModel):
    query_text: str = Field(..., description="The keyword to search for.")

class GooglePlacesSearchTool(BaseTool):
    name: str = "Google Places Search"
    description: str = (
        "Use this tool to search for places using the Google Places API. "
        "Provide a place name, type, or location keyword."
    )
    args_schema: Type[BaseModel] = GooglePlacesSearchInput

    def _run(self, query_text: str) -> str:
        url = "https://places.googleapis.com/v1/places:searchText"

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": API_KEY,
            "X-Goog-FieldMask": (
                "places.displayName,places.formattedAddress,"
                "places.location,places.photos"
            ),
        }

        payload = {
            "textQuery": query_text,
            "maxResultCount": 5,
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

            if "places" not in data:
                return "No places found."

            results = []
            for place in data["places"]:
                name = place.get("displayName", {}).get("text", "Unknown")
                address = place.get("formattedAddress", "No address")
                results.append(f"{name} - {address}")

            return "\n".join(results)

        except Exception as e:
            return f"Error while fetching places: {str(e)}"
