from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.database import get_db
from app.models.user import User
from app.models.annonce import Annonce, AnnonceStatus
from app.api.deps import require_admin

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/stats")
def get_stats(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return {
        "users": db.query(func.count(User.id)).scalar(),
        "annonces": db.query(func.count(Annonce.id)).scalar(),
        "active_annonces": db.query(func.count(Annonce.id)).filter(Annonce.status == AnnonceStatus.ACTIVE).scalar(),
        "total_views": db.query(func.sum(Annonce.views_count)).scalar() or 0,
    }

@router.get("/annonces/pending")
def pending(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return db.query(Annonce).filter(Annonce.status == AnnonceStatus.PENDING).all()

@router.put("/annonces/{annonce_id}/approve")
def approve(annonce_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    ann = db.query(Annonce).filter(Annonce.id == annonce_id).first()
    if not ann:
        raise HTTPException(404, "Introuvable")
    ann.status = AnnonceStatus.ACTIVE
    db.commit()
    return {"success": True}