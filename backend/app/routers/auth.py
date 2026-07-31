from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.citizen import Citizen
from app.models.officer import Officer
from app.schemas.auth import CitizenLogin, CitizenSignup, OfficerLogin, TokenResponse

router = APIRouter()


@router.post("/citizen/signup", response_model=TokenResponse)
def signup_citizen(payload: CitizenSignup, db: Session = Depends(get_db)):
    existing = db.query(Citizen).filter(Citizen.phone == payload.phone).first()
    if existing:
        raise HTTPException(status_code=400, detail="Citizen already exists")

    citizen = Citizen(
        name=payload.name,
        phone=payload.phone,
        hashed_password=get_password_hash(payload.password),
    )
    db.add(citizen)
    db.commit()
    db.refresh(citizen)

    token = create_access_token(str(citizen.id), extra_claims={"type": "citizen", "role": "citizen"})
    return TokenResponse(
        access_token=token,
        role="citizen",
        user={"id": citizen.id, "name": citizen.name, "type": "citizen"},
    )


@router.post("/citizen/login", response_model=TokenResponse)
def login_citizen(payload: CitizenLogin, db: Session = Depends(get_db)):
    citizen = db.query(Citizen).filter(Citizen.phone == payload.phone).first()
    if not citizen or not verify_password(payload.password, citizen.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(str(citizen.id), extra_claims={"type": "citizen", "role": "citizen"})
    return TokenResponse(
        access_token=token,
        role="citizen",
        user={"id": citizen.id, "name": citizen.name, "type": "citizen"},
    )


@router.post("/officer/login", response_model=TokenResponse)
def login_officer(payload: OfficerLogin, db: Session = Depends(get_db)):
    officer = db.query(Officer).filter(Officer.employee_id == payload.employee_id).first()
    if not officer or not verify_password(payload.password, officer.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(str(officer.id), extra_claims={"type": "officer", "role": officer.role.value})
    return TokenResponse(
        access_token=token,
        role=officer.role.value,
        ward=officer.ward,
        user={"id": officer.id, "name": officer.name, "role": officer.role.value, "type": "officer"},
    )
