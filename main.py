
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal
from models import Analysis

from get_ndvi import get_ndvi
from climate import get_climate_data
from risk_engine import analyze_risk

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/analyze")
def analyze(lat: float, lon: float):

    ndvi = get_ndvi(lat, lon)
    climate = get_climate_data(lat, lon)
    status, color = analyze_risk(ndvi, climate)

    db = SessionLocal()

    new_entry = Analysis(
        latitude=lat,
        longitude=lon,
        ndvi=ndvi,
        temperature=climate["temperature"] if climate else None,
        humidity=climate["humidity"] if climate else None,
        risk_status=status
    )

    db.add(new_entry)
    db.commit()
    db.close()

    return {
        "latitude": lat,
        "longitude": lon,
        "ndvi": ndvi,
        "climate": climate,
        "risk_status": status,
        "risk_color": color
    }

from fastapi import FastAPI
from climate import get_climate_data

app = FastAPI()

@app.get("/climate")
def climate(lat: float, lon: float):
    return get_climate_data(lat, lon)