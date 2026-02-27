from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Analysis(Base):
    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    ndvi = Column(Float)
    temperature = Column(Float)
    humidity = Column(Float)
    risk_status = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())