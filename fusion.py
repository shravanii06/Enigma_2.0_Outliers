# fusion.py

from config import TEMP_WEIGHT, NDWI_WEIGHT, NDVI_WEIGHT


def calculate_stress_score(temp, ndwi, ndvi):
    """
    Stress Score Formula:
    TEMP_WEIGHT * Temperature +
    NDWI_WEIGHT * (1 - NDWI) +
    NDVI_WEIGHT * (1 - NDVI)
    """

    stress_score = (
        TEMP_WEIGHT * temp +
        NDWI_WEIGHT * (1 - ndwi) +
        NDVI_WEIGHT * (1 - ndvi)
    )

    return round(stress_score, 3)



def calculate_risk_percentage(score):
    """
    Converts stress score (0–1) into percentage.
    """
    return round(score * 100, 2)


def classify_stress(score):
    if score < 0.3:
        return "Very Low Stress 🌿"
    elif score < 0.45:
        return "Low Stress 🍀"
    elif score < 0.6:
        return "Moderate Stress ⚠️"
    elif score < 0.75:
        return "High Stress 🔥"
    else:
        return "Severe Stress 🚨"


def explain_stress(temp, ndwi, ndvi):
    explanation = []

    if temp > 0.6:
        explanation.append("High Temperature contributing to stress.")
    else:
        explanation.append("Temperature is within safe range.")

    if ndwi < 0.4:
        explanation.append("Low Water Content detected.")
    else:
        explanation.append("Water levels are adequate.")

    if ndvi < 0.4:
        explanation.append("Vegetation health is poor.")
    else:
        explanation.append("Vegetation health looks good.")

    return " | ".join(explanation)