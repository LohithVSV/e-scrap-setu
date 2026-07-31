from pydantic import BaseModel


class DashboardSummary(BaseModel):
    ward: str | None = None
    total_collections: int
    total_weight_kg: float
    total_credits: int
    alerts: list[str]
