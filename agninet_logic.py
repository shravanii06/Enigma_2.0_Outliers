def process_farmer_query(text):
    text = text.lower()

    if "stress" in text or "yellow" in text:
        return "Your crop shows early water stress. Irrigation recommended within 3 days."
    
    if "risk" in text:
        return "Current crop health score is 82 out of 100. Risk level is moderate."
    
    if "irrigation" in text:
        return "Based on temperature and NDVI drop, irrigation is suggested soon."
    
    return "AgniNet detected normal crop condition. No immediate action required."