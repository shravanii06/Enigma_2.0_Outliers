from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
print("API KEY:", API_KEY)

def get_climate_data(lat: float, lon: float):
    if not API_KEY:
        return {"error": "API key not found"}

    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        )

        print("URL:", url)
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return {
                "error": "OpenWeather API failed",
                "status_code": response.status_code,
                "response": response.text
            }

        data = response.json()

        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"],
            "weather_condition": data["weather"][0]["description"]
        }

    except Exception as e:
        return {"error": str(e)}