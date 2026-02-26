def analyze_risk(ndvi, climate):

    if ndvi is None or climate is None:
        return "Unknown Risk", "gray"

    temp = climate.get("temperature", 0)
    humidity = climate.get("humidity", 0)

    # Critical condition
    if ndvi < 0.25 and temp > 40:
        return "🚨 CRITICAL ALERT: Crop Failure Risk", "red"

    # Severe vegetation stress
    if ndvi < 0.3:
        return "🔴 Severe Crop Stress", "red"

    # Heat stress
    if temp > 38:
        return "🔴 Heat Stress Risk", "red"

    # Drought risk
    if humidity < 30:
        return "🟡 Drought Risk", "orange"

    # Healthy
    if ndvi > 0.6:
        return "🟢 Healthy Crops", "green"

    return "🟡 Moderate Risk", "orange"