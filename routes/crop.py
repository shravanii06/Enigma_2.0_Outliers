from fastapi import APIRouter
from get_ndvi import get_ndvi
from climate import get_climate_data
from ai_engine import get_crop_suggestion

router = APIRouter()

@router.get("/crop-health")
def crop_health(lat: float, lon: float):

    ndvi = get_ndvi(lat, lon)
    climate = get_climate_data(lat, lon)
    suggestion = get_crop_suggestion(ndvi, climate)

    return {
        "ndvi": ndvi,
        "climate": climate,
        "suggestion": suggestion
    }