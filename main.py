
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from get_ndvi import get_ndvi
from climate import get_climate_data
from risk_engine import analyze_risk

from voice import speech_to_text, text_to_speech
from agninet_logic import process_farmer_query

app = FastAPI()

# -------------------------------
# CORS (Allow Frontend)
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Later restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Create Required Folders
# -------------------------------
UPLOAD_DIR = "uploads"
AUDIO_OUTPUT_DIR = "audio_outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)

# Serve audio files to frontend
app.mount("/audio_outputs", StaticFiles(directory="audio_outputs"), name="audio")


# =====================================================
# 🌾 CROP ANALYSIS ENDPOINT
# =====================================================
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