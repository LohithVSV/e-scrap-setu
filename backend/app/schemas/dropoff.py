from pydantic import BaseModel


class DropoffPointCreate(BaseModel):
    name: str
    ward: str
    latitude: float
    longitude: float
    qr_code: str
    capacity_kg: float = 100.0
    current_load_kg: float = 0.0
    threshold_pct: float = 75.0


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
