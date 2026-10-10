import json
import os
from sqlalchemy.orm import Session

from .core.database import SessionLocal, engine, Base
from .core.security import hash_password
from .models.db_models import User, Product, Address, Card, Basket, Feedback

HERE = os.path.dirname(__file__)


def _load(name: str):
    with open(os.path.join(HERE, "seed_data", name)) as f:
        return json.load(f)


def seed(db: Session):
    if db.query(Product).first():
        return  # already seeded

    for p in _load("products.json"):
        db.add(Product(
            id=p["id"],
            name=p["name"],
            description=p["description"],
            price=p["price"],
            image=p["image"],
            deleted=p["deleted"],
        ))
    db.commit()

    for u in _load("users.json"):
        user = User(
            id=u["id"],
            email=u["email"],
            hashed_password=hash_password(u["password"] or "ChangeMe123!"),
            role=u["role"],
            wallet_balance=u.get("wallet_balance") or 0,
            security_answer_hash=hash_password(u["security_question_answer"]) if u.get("security_question_answer") else None,
        )
        db.add(user)
        db.flush()

        db.add(Basket(user_id=user.id))

        for a in u.get("addresses") or []:
            db.add(Address(
                user_id=user.id,
                full_name=a.get("fullName"),
                mobile_num=str(a.get("mobileNum")),
                zip_code=str(a.get("zipCode")),
                street_address=a.get("streetAddress"),
                city=a.get("city"),
                state=a.get("state"),
                country=a.get("country"),
            ))

        for c in u.get("cards") or []:
            card_num = str(c.get("cardNum", ""))
            db.add(Card(
                user_id=user.id,
                full_name=c.get("fullName"),
                card_num_last4=card_num[-4:] if card_num else None,
                exp_month=c.get("expMonth"),
                exp_year=c.get("expYear"),
            ))

        fb = u.get("feedback")
        if fb:
            db.add(Feedback(user_id=user.id, comment=fb.get("comment"), rating=fb.get("rating")))

    db.commit()


def init_db_and_seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()
