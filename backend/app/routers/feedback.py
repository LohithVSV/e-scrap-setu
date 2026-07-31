from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate

router = APIRouter()


@router.post("", response_model=dict)
def submit_feedback(payload: FeedbackCreate, db: Session = Depends(get_db)):
    feedback = Feedback(rating=payload.stars, comment=payload.comment)
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return {"status": "submitted", "id": feedback.id}
