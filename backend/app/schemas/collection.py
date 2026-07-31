from datetime import datetime

from pydantic import BaseModel


class CollectionCreate(BaseModel):
    id: int | None = None
    dropoff_id: int | None = None
    dropoff_point_id: int | None = None
    citizen_id: int | None = None
    phone: str | None = None
    weight_kg: float | None = None
    item_type: str | None = None
    status: str | None = None


class CollectionOut(BaseModel):
    id: int
    dropoff_point_id: int
    citizen_id: int | None
    officer_id: int
    weight_kg: float
    item_type: str | None
    credits_awarded: int
    status: str | None = None
    citizen_name: str | None = None
    dropoff_point_name: str | None = None
    logged_at: datetime | None = None
