from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    type: str
    is_read: bool
    link: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AlertCreate(BaseModel):
    name: str
    keywords: Optional[str] = None
    category_id: Optional[int] = None
    city: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None


class AlertResponse(AlertCreate):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
    suggestions: List[dict] = []