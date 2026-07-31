from pydantic import BaseModel


class RewardRedeem(BaseModel):
    citizen_id: int | None = None
    phone: str | None = None
    amount: int
    item: str
