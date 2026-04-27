from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
from app.models.user import favorites_table
import enum

class AnnonceStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SOLD = "sold"
    PENDING = "pending"
    REJECTED = "rejected"

class AnnonceCondition(str, enum.Enum):
    NEW = "new"
    LIKE_NEW = "like_new"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    icon = Column(String(100))
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    parent = relationship("Category", remote_side=[id], back_populates="children")
    children = relationship("Category", back_populates="parent")
    annonces = relationship("Annonce", back_populates="category")

class Annonce(Base):
    __tablename__ = "annonces"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=True)
    is_negotiable = Column(Boolean, default=False)
    condition = Column(Enum(AnnonceCondition), default=AnnonceCondition.GOOD)
    status = Column(Enum(AnnonceStatus), default=AnnonceStatus.ACTIVE)
    city = Column(String(100), index=True)
    location = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    views_count = Column(Integer, default=0)
    clicks_count = Column(Integer, default=0)
    tags = Column(JSON, default=list)
    ai_category_suggestion = Column(String(100))
    embedding = Column(JSON)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    owner = relationship("User", back_populates="annonces")
    category = relationship("Category", back_populates="annonces")
    images = relationship("AnnonceImage", back_populates="annonce", cascade="all, delete-orphan")
    favorited_by = relationship("User", secondary=favorites_table, back_populates="favorites")
    interactions = relationship("UserInteraction", back_populates="annonce", cascade="all, delete-orphan")

class AnnonceImage(Base):
    __tablename__ = "annonce_images"
    id = Column(Integer, primary_key=True, index=True)
    annonce_id = Column(Integer, ForeignKey("annonces.id"), nullable=False)
    url = Column(String(500), nullable=False)
    is_primary = Column(Boolean, default=False)
    order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    annonce = relationship("Annonce", back_populates="images")