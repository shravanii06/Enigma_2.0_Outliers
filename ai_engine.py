def get_crop_suggestion(ndvi, climate):
    """
    Generates crop suggestions based on NDVI and climate data.
    """

    suggestions = []

    # NDVI based suggestion
    if ndvi is not None:
        if ndvi < 40:
            suggestions.append("Low vegetation detected → Irrigation recommended")
        elif ndvi < 60:
            suggestions.append("Moderate vegetation → Monitor crop health")
        else:
            suggestions.append("Good vegetation growth")

    # Climate based suggestions
    if climate is not None:

        temperature = climate.get("temperature")
        humidity = climate.get("humidity")

        if humidity is not None and humidity > 80:
            suggestions.append("High humidity → Risk of fungal disease")

        if temperature is not None and temperature > 35:
            suggestions.append("High temperature → Heat stress risk")

        if temperature is not None and temperature < 10:
            suggestions.append("Low temperature → Frost risk")

    # If nothing triggered
    if not suggestions:
        suggestions.append("Crop condition looks healthy")

    return suggestions