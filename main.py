
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

DATABASE_URL = "sqlite:///./crop.db"   

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Analysis(Base):
    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    ndvi = Column(Float)
    temperature = Column(Float)
    humidity = Column(Float)
    risk_status = Column(String)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_ndvi(lat, lon):
   
    return 65

def get_climate_data(lat, lon):

    if not API_KEY:
        return None

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["description"]
    }

def analyze_risk(ndvi, climate):

    if ndvi < 40:
        return "High Risk", "red"

    if climate and climate["temperature"] > 35:
        return "Moderate Risk", "orange"

    return "Low Risk", "green"

def get_crop_suggestion(ndvi, climate):

    suggestions = []

    if ndvi < 40:
        suggestions.append("Low vegetation → Irrigation needed")

    if climate and climate["humidity"] > 80:
        suggestions.append("High humidity → Fungal disease risk")

    if climate and climate["temperature"] > 35:
        suggestions.append("High temperature → Heat stress")

    if not suggestions:
        suggestions.append("Crop looks healthy")

    return suggestions

@app.get("/analyze")
def analyze(lat: float, lon: float):

    ndvi = get_ndvi(lat, lon)
    climate = get_climate_data(lat, lon)
    risk_status, risk_color = analyze_risk(ndvi, climate)
    suggestion = get_crop_suggestion(ndvi, climate)

    db = SessionLocal()

    new_entry = Analysis(
        latitude=lat,
        longitude=lon,
        ndvi=ndvi,
        temperature=climate["temperature"] if climate else None,
        humidity=climate["humidity"] if climate else None,
        risk_status=risk_status
    )

    db.add(new_entry)
    db.commit()
    db.close()

    return {
        "latitude": lat,
        "longitude": lon,
        "ndvi": ndvi,
        "climate": climate,
        "risk_status": risk_status,
        "risk_color": risk_color,
        "suggestion": suggestion
    }