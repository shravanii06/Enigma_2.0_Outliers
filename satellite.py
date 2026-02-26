
import random
def get_comparison_data():
    """
    Returns mock current vs baseline data for NDVI, NDWI, and Temperature.
    """
    current_data = {'ndvi': 0.75, 'ndwi': 0.41, 'temp': 0.70}   
    baseline_data = {'ndvi': 0.40, 'ndwi': 0.38, 'temp': 0.82} 
    return current_data, baseline_data
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