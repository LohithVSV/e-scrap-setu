from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.citizen import Citizen
from app.models.collection import Collection
from app.models.dropoff import DropoffPoint
from app.models.officer import Officer
from app.schemas.collection import CollectionCreate, CollectionOut

router = APIRouter()


def serialize_collection(collection: Collection) -> CollectionOut:
    return CollectionOut(
        id=collection.id,
        dropoff_point_id=collection.dropoff_point_id,
        citizen_id=collection.citizen_id,
        officer_id=collection.officer_id,
        weight_kg=collection.weight_kg,
        item_type=collection.item_type,
        credits_awarded=collection.credits_awarded,
        status=getattr(collection, "status", None),
        citizen_name=collection.citizen.name if collection.citizen else None,
        dropoff_point_name=collection.dropoff_point.name if collection.dropoff_point else None,
        logged_at=collection.logged_at,
    )


@router.get("", response_model=list[CollectionOut])
def list_collections(db: Session = Depends(get_db)):
    collections = (
        db.query(Collection)
        .join(DropoffPoint, Collection.dropoff_point_id == DropoffPoint.id, isouter=True)
        .join(Citizen, Collection.citizen_id == Citizen.id, isouter=True)
        .order_by(Collection.id.desc())
        .all()
    )
    return [serialize_collection(item) for item in collections]


@router.get("/ward/{ward_id}", response_model=list[CollectionOut])
def list_ward_collections(ward_id: str, db: Session = Depends(get_db)):
    collections = (
        db.query(Collection)
        .join(DropoffPoint, Collection.dropoff_point_id == DropoffPoint.id)
        .join(Citizen, Collection.citizen_id == Citizen.id, isouter=True)
        .filter(DropoffPoint.ward == ward_id)
        .order_by(Collection.id.desc())
        .all()
    )
    return [serialize_collection(item) for item in collections]


@router.post("", response_model=CollectionOut)
def create_collection(payload: CollectionCreate, db: Session = Depends(get_db)):
    officer = db.query(Officer).first()
    if not officer:
        officer = Officer(name="Demo Officer", employee_id="demo-officer", hashed_password="", role="field_officer")
        db.add(officer)
        db.commit()
        db.refresh(officer)

    dropoff_id = payload.dropoff_point_id or payload.dropoff_id
    if dropoff_id is None:
        raise HTTPException(status_code=400, detail="dropoff_id is required")

    dropoff = db.query(DropoffPoint).filter(DropoffPoint.id == dropoff_id).first()
    if not dropoff:
        raise HTTPException(status_code=404, detail="Drop-off point not found")

    citizen = None
    if payload.citizen_id is not None:
        citizen = db.query(Citizen).filter(Citizen.id == payload.citizen_id).first()
    elif payload.phone:
        citizen = db.query(Citizen).filter(Citizen.phone == payload.phone).first()

    if payload.citizen_id is not None and citizen is None:
        raise HTTPException(status_code=404, detail="Citizen not found")
    if payload.phone and citizen is None:
        raise HTTPException(status_code=404, detail="Citizen not found")

    if payload.id is not None:
        collection = db.query(Collection).filter(Collection.id == payload.id).first()
        if not collection:
            raise HTTPException(status_code=404, detail="Collection not found")
        collection.status = payload.status or collection.status
        db.commit()
        db.refresh(collection)
        return serialize_collection(collection)

    credits = max(1, int((payload.weight_kg or 0) * 10)) if payload.weight_kg is not None else 1
    collection = Collection(
        dropoff_point_id=dropoff_id,
        citizen_id=payload.citizen_id,
        officer_id=officer.id,
        weight_kg=payload.weight_kg or 0.0,
        item_type=payload.item_type,
        credits_awarded=credits,
        status=payload.status or "pending_officer_confirmation",
    )
    db.add(collection)
    if citizen is not None:
        citizen.credits += collection.credits_awarded
    db.commit()
    db.refresh(collection)
    return serialize_collection(collection)
