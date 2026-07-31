# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from models import RoleEnum

# --- Auth ---
class CitizenSignup(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    password: str

class CitizenLogin(BaseModel):
    email: EmailStr
    password: str

class OfficerLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: Optional[str] = None

# --- Dropoff points ---
class DropoffPointOut(BaseModel):
    id: int
    name: str
    ward: str
    latitude: float
    longitude: float
    qr_code: str
    capacity_kg: float
    current_load_kg: float
    threshold_pct: float

    class Config:
        from_attributes = True

# --- Collections ---
class CollectionCreate(BaseModel):
    dropoff_point_id: int
    citizen_id: Optional[int] = None
    weight_kg: float
    item_type: Optional[str] = None

class CollectionOut(BaseModel):
    id: int
    dropoff_point_id: int
    citizen_id: Optional[int]
    officer_id: int
    weight_kg: float
    item_type: Optional[str]
    credits_awarded: int
    logged_at: datetime

    class Config:
        from_attributes = True

# --- Rewards ---
class RedeemRequest(BaseModel):
    reward_name: str
    credits_cost: int

# --- Feedback ---
class FeedbackCreate(BaseModel):
    citizen_id: Optional[int] = None
    dropoff_point_id: Optional[int] = None
    rating: int
    comment: Optional[str] = None

# --- Dashboard ---
class WardStats(BaseModel):
    ward: str
    total_collections: int
    total_weight_kg: float
    active_alerts: int