
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
import uuid

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
    allow_origins=["*"],  # Restrict in production
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

    return {
        "latitude": lat,
        "longitude": lon,
        "ndvi": ndvi,
        "climate": climate,
        "risk_status": status,
        "risk_color": color
    }


# =====================================================
# 🎤 VOICE AGENT ENDPOINT
# =====================================================
@app.post("/voice-agent/")
async def voice_agent(audio: UploadFile = File(...)):

    # Save uploaded audio
    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.wav")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    # 1️⃣ Speech → Text
    user_text, detected_lang = speech_to_text(file_path)

    # 2️⃣ Process Farmer Query
    response_text = process_farmer_query(user_text)

    # 3️⃣ Decide language for reply
    if detected_lang == "hi":
        lang = "hi"
    else:
        lang = "en"

    # 4️⃣ Text → Speech
    audio_response_path = text_to_speech(response_text, lang=lang)

    # Return relative URL for frontend
    audio_filename = os.path.basename(audio_response_path)

    return {
        "user_text": user_text,
        "response_text": response_text,
        "audio_url": f"/audio_outputs/{audio_filename}"
    }