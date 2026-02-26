# fusion.py

def calculate_stress_score(temp, ndwi, ndvi):
    """
    Calculate overall stress score (0 to 1)
    """
    return round(0.4*temp + 0.3*(1-ndwi) + 0.3*(1-ndvi), 3)

def classify_stress(score):
    """
    Classify stress based on score
    """
    if score < 0.4:
        return "Low Stress"
    elif score < 0.6:
        return "Moderate Stress"
    else:
        return "High Stress"

def get_stress_color(score):
    """
    Return color for stress level
    """
    if score < 0.4:
        return "green"
    elif score < 0.6:
        return "orange"
    else:
        return "red"