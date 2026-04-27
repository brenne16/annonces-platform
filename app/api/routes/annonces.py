from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from typing import List, Optional
import os, uuid, aiofiles

from app.db.database import get_db
from app.models.annonce import Annonce, AnnonceImage, AnnonceStatus, Category
from app.models.interaction import UserInteraction, InteractionType
from app.models.user import User
from app.schemas.annonce import AnnonceResponse, AnnonceListResponse, AnnonceUpdate, CategoryCreate, CategoryResponse
from app.api.deps import get_current_user, get_optional_user, require_admin
from app.core.config import settings

router = APIRouter(prefix="/annonces", tags=["Annonces"])

@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).filter(Category.parent_id == None).all()

@router.post("/categories", response_model=CategoryResponse, status_code=201)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    cat = Category(**payload.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

@router.get("", response_model=AnnonceListResponse)
def list_annonces(
    q: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    city: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    sort_by: str = Query("created_at"),
    order: str = Query("desc"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
):
    query = db.query(Annonce).filter(Annonce.status == AnnonceStatus.ACTIVE)
    if q:
        query = query.filter(or_(Annonce.title.ilike(f"%{q}%"), Annonce.description.ilike(f"%{q}%")))
        if current_user:
            db.add(UserInteraction(user_id=current_user.id, interaction_type=InteractionType.SEARCH, search_query=q))
            db.commit()
    if category_id:
        query = query.filter(Annonce.category_id == category_id)
    if city:
        query = query.filter(Annonce.city.ilike(f"%{city}%"))
    if min_price is not None:
        query = query.filter(Annonce.price >= min_price)
    if max_price is not None:
        query = query.filter(Annonce.price <= max_price)
    sort_col = getattr(Annonce, sort_by, Annonce.created_at)
    query = query.order_by(desc(sort_col) if order == "desc" else asc(sort_col))
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    return AnnonceListResponse(items=items, total=total, page=page, pages=(total + per_page - 1) // per_page, per_page=per_page)

@router.post("", response_model=AnnonceResponse, status_code=201)
async def create_annonce(
    title: str = Form(...),
    description: str = Form(...),
    price: Optional[float] = Form(None),
    is_negotiable: bool = Form(False),
    condition: str = Form("good"),
    city: Optional[str] = Form(None),
    category_id: Optional[int] = Form(None),
    images: List[UploadFile] = File(default=[]),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    annonce = Annonce(
        title=title, description=description, price=price,
        is_negotiable=is_negotiable, condition=condition,
        city=city, category_id=category_id, owner_id=current_user.id, tags=[],
    )
    db.add(annonce)
    db.flush()
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    for i, img in enumerate(images[:5]):
        ext = img.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        path = os.path.join(settings.UPLOAD_DIR, filename)
        async with aiofiles.open(path, "wb") as f:
            await f.write(await img.read())
        db.add(AnnonceImage(annonce_id=annonce.id, url=f"/uploads/{filename}", is_primary=(i == 0), order=i))
    db.commit()
    db.refresh(annonce)
    return annonce

@router.get("/{annonce_id}", response_model=AnnonceResponse)
def get_annonce(annonce_id: int, db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_optional_user)):
    annonce = db.query(Annonce).filter(Annonce.id == annonce_id).first()
    if not annonce:
        raise HTTPException(404, "Annonce introuvable")
    annonce.views_count += 1
    if current_user:
        db.add(UserInteraction(user_id=current_user.id, annonce_id=annonce_id, interaction_type=InteractionType.VIEW))
    db.commit()
    db.refresh(annonce)
    return annonce

@router.put("/{annonce_id}", response_model=AnnonceResponse)
def update_annonce(annonce_id: int, payload: AnnonceUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    annonce = db.query(Annonce).filter(Annonce.id == annonce_id).first()
    if not annonce:
        raise HTTPException(404, "Annonce introuvable")
    if annonce.owner_id != current_user.id:
        raise HTTPException(403, "Accès refusé")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(annonce, field, value)
    db.commit()
    db.refresh(annonce)
    return annonce

@router.delete("/{annonce_id}", status_code=204)
def delete_annonce(annonce_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    annonce = db.query(Annonce).filter(Annonce.id == annonce_id).first()
    if not annonce:
        raise HTTPException(404, "Annonce introuvable")
    if annonce.owner_id != current_user.id:
        raise HTTPException(403, "Accès refusé")
    db.delete(annonce)
    db.commit()

@router.post("/{annonce_id}/favorite")
def toggle_favorite(annonce_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    annonce = db.query(Annonce).filter(Annonce.id == annonce_id).first()
    if not annonce:
        raise HTTPException(404, "Annonce introuvable")
    if annonce in current_user.favorites:
        current_user.favorites.remove(annonce)
        db.commit()
        return {"favorited": False}
    current_user.favorites.append(annonce)
    db.commit()
    return {"favorited": True}