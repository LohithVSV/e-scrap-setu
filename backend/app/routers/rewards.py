from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.citizen import Citizen
from app.models.redemption import Redemption
from app.schemas.reward import RewardRedeem

router = APIRouter()


@router.get("/phone/{phone}")
def get_citizen_rewards_by_phone(phone: str, db: Session = Depends(get_db)):
    citizen = db.query(Citizen).filter(Citizen.phone == phone).first()
    if not citizen:
        raise HTTPException(status_code=404, detail="Citizen not found")
    return {"citizen_id": citizen.id, "phone": citizen.phone, "credits": citizen.credits, "redemptions": []}


@router.get("/{citizen_id:int}")
def get_citizen_rewards(citizen_id: int, db: Session = Depends(get_db)):
    citizen = db.query(Citizen).filter(Citizen.id == citizen_id).first()
    if not citizen:
        raise HTTPException(status_code=404, detail="Citizen not found")
    return {"citizen_id": citizen.id, "credits": citizen.credits, "redemptions": []}


@router.post("/redeem")
def redeem_rewards(payload: RewardRedeem, db: Session = Depends(get_db)):
    citizen = None
    if payload.citizen_id is not None:
        citizen = db.query(Citizen).filter(Citizen.id == payload.citizen_id).first()
    elif payload.phone:
        citizen = db.query(Citizen).filter(Citizen.phone == payload.phone).first()

    if not citizen:
        raise HTTPException(status_code=404, detail="Citizen not found")
    if citizen.credits < payload.amount:
        raise HTTPException(status_code=400, detail="Insufficient credits")

    citizen.credits -= payload.amount
    redemption = Redemption(citizen_id=citizen.id, reward_name=payload.item, credits_spent=payload.amount)
    db.add(redemption)
    db.commit()
    return {"status": "redeemed", "citizen_id": citizen.id, "remaining_credits": citizen.credits}
