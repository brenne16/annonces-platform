import sys
sys.path.insert(0, ".")

from app.db.database import SessionLocal, Base, engine
from app.models.user import User, UserRole
from app.models.annonce import Category, Annonce, AnnonceCondition, AnnonceStatus
from app.core.security import get_password_hash

Base.metadata.create_all(bind=engine)
db = SessionLocal()

categories = [
    {"name": "Immobilier", "slug": "immobilier", "icon": "🏠"},
    {"name": "Véhicules", "slug": "vehicules", "icon": "🚗"},
    {"name": "Électronique", "slug": "electronique", "icon": "📱"},
    {"name": "Mode", "slug": "mode", "icon": "👗"},
    {"name": "Maison", "slug": "maison", "icon": "🛋️"},
    {"name": "Sports", "slug": "sports", "icon": "⚽"},
    {"name": "Emploi", "slug": "emploi", "icon": "💼"},
    {"name": "Animaux", "slug": "animaux", "icon": "🐾"},
    {"name": "Autre", "slug": "autre", "icon": "📦"},
]
for c in categories:
    if not db.query(Category).filter(Category.slug == c["slug"]).first():
        db.add(Category(**c))
db.commit()
print("✅ Catégories créées")

users_data = [
    {"email": "admin@annonces.ma", "username": "admin", "password": "Admin1234!", "role": UserRole.ADMIN, "city": "Casablanca"},
    {"email": "user@annonces.ma", "username": "demo_user", "password": "User1234!", "role": UserRole.USER, "city": "Rabat"},
]
for u in users_data:
    if not db.query(User).filter(User.email == u["email"]).first():
        pw = u.pop("password")
        db.add(User(**u, hashed_password=get_password_hash(pw), is_verified=True))
db.commit()
print("✅ Utilisateurs créés")

owner = db.query(User).filter(User.username == "demo_user").first()
cat = db.query(Category).filter(Category.slug == "electronique").first()
if not db.query(Annonce).filter(Annonce.title == "iPhone 14 Pro").first():
    db.add(Annonce(
        title="iPhone 14 Pro", description="Très bon état, avec boîte",
        price=9500, is_negotiable=True, condition=AnnonceCondition.LIKE_NEW,
        city="Casablanca", category_id=cat.id, owner_id=owner.id,
        status=AnnonceStatus.ACTIVE, tags=["iphone", "apple"]
    ))
db.commit()
print("✅ Annonces créées")
print("\n🎉 Seed terminé !")
print("Admin  → admin@annonces.ma / Admin1234!")
print("User   → user@annonces.ma / User1234!")
db.close()