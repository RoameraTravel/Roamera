import requests
from datetime import datetime

def get_forecast_for_day(lat, lon, target_date):
    # 1. Get point metadata
    points_url = f"https://api.weather.gov/points/{lat},{lon}"
    r = requests.get(points_url)
    r.raise_for_status()
    data = r.json()

    forecast_url = data['properties']['forecast']

    # 2. Get forecast data
    r = requests.get(forecast_url)
    r.raise_for_status()
    forecast_data = r.json()

    # 3. Filter for target_date
    target_date = datetime.strptime(target_date, "%Y-%m-%d").date()
    for period in forecast_data['properties']['periods']:
        start_time = datetime.fromisoformat(period['startTime']).date()
        if start_time == target_date:
            return period

    return None

# Example usage:
forecast = get_forecast_for_day(40.7128, -74.0060, "2025-08-05")
if forecast:
    print(f"Forecast on {forecast['name']}: {forecast['shortForecast']}, Temp: {forecast['temperature']} {forecast['temperatureUnit']}")
else:
    print("No forecast found for that date.")
