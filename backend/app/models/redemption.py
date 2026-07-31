from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Redemption(Base):
    __tablename__ = "redemptions"

    id = Column(Integer, primary_key=True, index=True)
    citizen_id = Column(Integer, ForeignKey("citizens.id"), nullable=False)
    reward_name = Column(String, nullable=False)
    credits_spent = Column(Integer, nullable=False)
    redeemed_at = Column(DateTime, default=datetime.utcnow)

    citizen = relationship("Citizen", back_populates="redemptions")
