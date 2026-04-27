from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime
from app.models.annonce import AnnonceStatus, AnnonceCondition
from app.schemas.user import UserPublic

class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    icon: Optional[str] = None

class CategoryCreate(CategoryBase):
    parent_id: Optional[int] = None

class CategoryResponse(CategoryBase):
    id: int
    parent_id: Optional[int] = None
    children: List["CategoryResponse"] = []
    class Config:
        from_attributes = True

CategoryResponse.model_rebuild()

class AnnonceImageResponse(BaseModel):
    id: int
    url: str
    is_primary: bool
    order: int
    class Config:
        from_attributes = True

class AnnonceBase(BaseModel):
    title: str
    description: str
    price: Optional[float] = None
    is_negotiable: bool = False
    condition: AnnonceCondition = AnnonceCondition.GOOD
    city: Optional[str] = None
    location: Optional[str] = None
    category_id: Optional[int] = None

class AnnonceCreate(AnnonceBase):
    pass

class AnnonceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_negotiable: Optional[bool] = None
    condition: Optional[AnnonceCondition] = None
    city: Optional[str] = None
    location: Optional[str] = None
    category_id: Optional[int] = None
    status: Optional[AnnonceStatus] = None

class AnnonceResponse(AnnonceBase):
    id: int
    status: AnnonceStatus
    views_count: int
    clicks_count: int
    tags: List[str] = []
    ai_category_suggestion: Optional[str] = None
    owner: UserPublic
    images: List[AnnonceImageResponse] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class AnnonceListResponse(BaseModel):
    items: List[AnnonceResponse]
    total: int
    page: int
    pages: int
    per_page: int