
import random

def generate_mock_day():
    return {
        "ndvi": round(random.uniform(0.4, 0.9), 3),
        "ndwi": round(random.uniform(0.2, 0.8), 3),
        "temp": round(random.uniform(0.3, 0.9), 3)
    }

def get_comparison_data():
    day1 = generate_mock_day()
    day7 = generate_mock_day()
    return day1, day7