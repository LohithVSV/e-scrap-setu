from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    dropoff_point_id = Column(Integer, ForeignKey("dropoff_points.id"), nullable=False)
    citizen_id = Column(Integer, ForeignKey("citizens.id"), nullable=True)
    officer_id = Column(Integer, ForeignKey("officers.id"), nullable=False)
    weight_kg = Column(Float, nullable=False)
    item_type = Column(String, nullable=True)
    credits_awarded = Column(Integer, default=0)
    status = Column(String, default="pending_officer_confirmation")
    logged_at = Column(DateTime, default=datetime.utcnow)

    dropoff_point = relationship("DropoffPoint", back_populates="collections")
    citizen = relationship("Citizen", back_populates="collections")
