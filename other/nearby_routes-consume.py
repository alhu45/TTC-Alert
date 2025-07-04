import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Your API key
api_key = os.getenv("TRANSIT_API")

# Set headers with apiKey
headers = {
    "apiKey": api_key
}

# Parameters for the request
params = {
    "lat": 43.801632,
    "lon": -79.447420,
    "max_distance": 1000,
    "should_update_realtime": True
}

# Make the GET request
response = requests.get("https://external.transitapp.com/v3/public/nearby_routes", headers=headers, params=params)

# Print results
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
