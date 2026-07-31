from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Citizen(Base):
    __tablename__ = "citizens"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    credits = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    collections = relationship("Collection", back_populates="citizen")
    redemptions = relationship("Redemption", back_populates="citizen")
