# models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base

class RoleEnum(str, enum.Enum):
    field_officer = "field_officer"
    supervisor = "supervisor"
    zonal_officer = "zonal_officer"
    commissioner = "commissioner"

class Citizen(Base):
    __tablename__ = "citizens"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    credits = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    collections = relationship("Collection", back_populates="citizen")
    redemptions = relationship("Redemption", back_populates="citizen")

class Officer(Base):
    __tablename__ = "officers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    ward = Column(String, nullable=True)  # null for commissioner/zonal (cross-ward)
    created_at = Column(DateTime, default=datetime.utcnow)

class DropoffPoint(Base):
    __tablename__ = "dropoff_points"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ward = Column(String, nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    qr_code = Column(String, unique=True, nullable=False)  # encoded string used in QR
    capacity_kg = Column(Float, default=100.0)
    current_load_kg = Column(Float, default=0.0)
    threshold_pct = Column(Float, default=75.0)  # triggers alert above this %

    collections = relationship("Collection", back_populates="dropoff_point")

class Collection(Base):
    __tablename__ = "collections"
    id = Column(Integer, primary_key=True, index=True)
    dropoff_point_id = Column(Integer, ForeignKey("dropoff_points.id"), nullable=False)
    citizen_id = Column(Integer, ForeignKey("citizens.id"), nullable=True)  # nullable: walk-in
    officer_id = Column(Integer, ForeignKey("officers.id"), nullable=False)
    weight_kg = Column(Float, nullable=False)
    item_type = Column(String, nullable=True)
    credits_awarded = Column(Integer, default=0)
    logged_at = Column(DateTime, default=datetime.utcnow)

    dropoff_point = relationship("DropoffPoint", back_populates="collections")
    citizen = relationship("Citizen", back_populates="collections")

class Redemption(Base):
    __tablename__ = "redemptions"
    id = Column(Integer, primary_key=True, index=True)
    citizen_id = Column(Integer, ForeignKey("citizens.id"), nullable=False)
    reward_name = Column(String, nullable=False)
    credits_spent = Column(Integer, nullable=False)
    redeemed_at = Column(DateTime, default=datetime.utcnow)

    citizen = relationship("Citizen", back_populates="redemptions")

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    citizen_id = Column(Integer, ForeignKey("citizens.id"), nullable=True)
    dropoff_point_id = Column(Integer, ForeignKey("dropoff_points.id"), nullable=True)
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)