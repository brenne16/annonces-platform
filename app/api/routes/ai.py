from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import uuid

from app.db.database import get_db
from app.models.annonce import Annonce, AnnonceStatus
from app.models.interaction import ChatMessage, UserInteraction, InteractionType
from app.models.user import User
from app.schemas.misc import ChatRequest, ChatResponse
from app.api.deps import get_current_user, get_optional_user

router = APIRouter(tags=["IA"])

@router.get("/annonces/{annonce_id}/similar")
def get_similar(annonce_id: int, db: Session = Depends(get_db)):
    annonce = db.query(Annonce).filter(Annonce.id == annonce_id).first()
    if not annonce:
        raise HTTPException(404, "Annonce introuvable")
    query = db.query(Annonce).filter(Annonce.id != annonce_id, Annonce.status == AnnonceStatus.ACTIVE)
    if annonce.category_id:
        query = query.filter(Annonce.category_id == annonce.category_id)
    return query.limit(6).all()

@router.get("/recommendations")
def get_recommendations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    interactions = db.query(UserInteraction).filter(
        UserInteraction.user_id == current_user.id,
        UserInteraction.annonce_id != None
    ).all()
    viewed_ids = {i.annonce_id for i in interactions}
    category_score = {}
    for inter in interactions:
        ann = db.query(Annonce).filter(Annonce.id == inter.annonce_id).first()
        if ann and ann.category_id:
            w = 3.0 if inter.interaction_type == InteractionType.FAVORITE else 1.0
            category_score[ann.category_id] = category_score.get(ann.category_id, 0) + w
    if not category_score:
        return db.query(Annonce).filter(Annonce.status == AnnonceStatus.ACTIVE).order_by(Annonce.views_count.desc()).limit(10).all()
    top_cats = sorted(category_score, key=category_score.get, reverse=True)[:3]
    return db.query(Annonce).filter(
        Annonce.status == AnnonceStatus.ACTIVE,
        Annonce.category_id.in_(top_cats),
        ~Annonce.id.in_(viewed_ids)
    ).limit(10).all()

@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_optional_user)):
    session_id = payload.session_id or str(uuid.uuid4())
    return ChatResponse(
        response=f"Bonjour ! Je suis votre assistant. Vous avez demandé : '{payload.message}'. Comment puis-je vous aider à trouver une annonce ?",
        session_id=session_id,
        suggestions=[]
    )