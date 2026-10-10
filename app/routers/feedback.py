from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from ..core.database import get_db
from ..core.security import get_current_user_optional
from ..models.db_models import User, Feedback
from ..models.schemas import FeedbackIn, FeedbackOut

router = APIRouter(prefix="/api/feedback", tags=["feedback"])


@router.get("", response_model=list[FeedbackOut])
def list_feedback(db: Session = Depends(get_db)):
    return db.query(Feedback).order_by(Feedback.created_at.desc()).limit(100).all()


@router.post("", response_model=FeedbackOut, status_code=201)
def submit_feedback(
    payload: FeedbackIn,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    feedback = Feedback(
        user_id=current_user.id if current_user else None,
        comment=payload.comment,
        rating=payload.rating,
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback
