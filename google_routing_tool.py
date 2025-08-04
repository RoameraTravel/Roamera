from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests

# Replace with your actual Google Routes API key
API_KEY = "AIzaSyBPcU-aFgssg7jzuvuzCBUuNKlL2-EbsQo"

class GoogleRoutesInput(BaseModel):
    origin: str = Field(..., description="Starting point address or place name.")
    destination: str = Field(..., description="Ending point address or place name.")
    travel_mode: str = Field("DRIVE", description="Mode of travel: DRIVE, WALK, BICYCLE, TRANSIT")

class GoogleRoutesTool(BaseTool):
    name: str = "Google Routes"
    description: str = (
        "Use this tool to calculate routes and directions between an origin and a destination using the Google Routes API."
    )
    args_schema: Type[BaseModel] = GoogleRoutesInput

    def _run(self, origin: str, destination: str, travel_mode: str = "DRIVE") -> str:
        url = "https://routes.googleapis.com/directions/v2:computeRoutes"

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": API_KEY,
        }

        payload = {
            "origin": {"waypointType": "PLACE_ID", "placeId": origin} if origin.startswith("Ch") else {"query": origin},
            "destination": {"waypointType": "PLACE_ID", "placeId": destination} if destination.startswith("Ch") else {"query": destination},
            "travelMode": travel_mode,
            "routingPreference": "TRAFFIC_AWARE",
            "computeAlternativeRoutes": False,
            "languageCode": "en",
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

            routes = data.get("routes", [])
            if not routes:
                return "No routes found."

            route = routes[0]
            legs = route.get("legs", [])
            if not legs:
                return "No legs found in the route."

            steps_summary = []
            for leg in legs:
                for step in leg.get("steps", []):
                    instruction = step.get("maneuver", {}).get("instruction", {}).get("text", "")
                    distance_meters = step.get("distanceMeters", 0)
                    steps_summary.append(f"{instruction} ({distance_meters} meters)")

            return "Route directions:\n" + "\n".join(steps_summary)

        except Exception as e:
            return f"Error while fetching route: {str(e)}"
