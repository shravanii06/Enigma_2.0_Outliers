import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_climate_data(lat: float, lon: float):
    """
    Fetch real-time climate data from OpenWeather API
    """

    if not API_KEY:
        print("OpenWeather API key not found in .env")
        return None

    try:
        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        )

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print("OpenWeather API Error:", response.text)
            return None

        data = response.json()

        climate_data = {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"],
            "weather_condition": data["weather"][0]["description"]
        }

        return climate_data

    except Exception as e:
        print("Climate Fetch Error:", e)
        return None