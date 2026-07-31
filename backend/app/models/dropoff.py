from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class DropoffPoint(Base):
    __tablename__ = "dropoff_points"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ward = Column(String, nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    qr_code = Column(String, unique=True, nullable=False)
    capacity_kg = Column(Float, default=100.0)
    current_load_kg = Column(Float, default=0.0)
    threshold_pct = Column(Float, default=75.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    collections = relationship("Collection", back_populates="dropoff_point")
