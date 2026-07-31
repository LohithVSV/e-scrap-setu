from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.dropoff import DropoffPoint
from app.schemas.dropoff import DropoffPointCreate, DropoffPointOut

router = APIRouter()


@router.get("", response_model=list[DropoffPointOut])
def list_dropoffs(ward: str | None = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(DropoffPoint)
    if ward:
        query = query.filter(DropoffPoint.ward == ward)
    return query.order_by(DropoffPoint.id).all()


@router.post("", response_model=DropoffPointOut)
def create_dropoff(payload: DropoffPointCreate, db: Session = Depends(get_db)):
    dropoff = DropoffPoint(**payload.model_dump())
    db.add(dropoff)
    db.commit()
    db.refresh(dropoff)
    return dropoff


@router.get("/qr/{qr_code}", response_model=DropoffPointOut)
def get_dropoff_by_qr(qr_code: str, db: Session = Depends(get_db)):
    dropoff = db.query(DropoffPoint).filter(DropoffPoint.qr_code == qr_code).first()
    if not dropoff:
        raise HTTPException(status_code=404, detail="Drop-off point not found")
    return dropoff
