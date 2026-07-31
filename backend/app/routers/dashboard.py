from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.collection import Collection
from app.models.dropoff import DropoffPoint
from app.schemas.dashboard import DashboardSummary

router = APIRouter()


@router.get("/ward/{ward_id}", response_model=DashboardSummary)
def ward_dashboard(ward_id: str, db: Session = Depends(get_db)):
    collections = (
        db.query(Collection)
        .join(DropoffPoint, Collection.dropoff_point_id == DropoffPoint.id)
        .filter(DropoffPoint.ward == ward_id)
        .all()
    )
    total_weight = sum(item.weight_kg for item in collections)
    total_credits = sum(item.credits_awarded for item in collections)
    alerts = []
    if total_weight > 0:
        alerts.append(f"{ward_id} has active collections")
    return DashboardSummary(
        ward=ward_id,
        total_collections=len(collections),
        total_weight_kg=round(total_weight, 2),
        total_credits=total_credits,
        alerts=alerts,
    )


@router.get("/alerts", response_model=list[str])
def alerts(db: Session = Depends(get_db)):
    return ["No critical alerts"]
