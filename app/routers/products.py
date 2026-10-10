from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..core.database import get_db
from ..models.db_models import Product, Review, User
from ..models.schemas import ProductOut, ReviewIn, ReviewOut
from ..core.security import get_current_user

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("", response_model=list[ProductOut])
def list_products(
    q: Optional[str] = Query(default=None, description="Search by name"),
    limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    query = db.query(Product).filter(Product.deleted == False)  # noqa: E712
    if q:
        query = query.filter(Product.name.ilike(f"%{q}%"))
    return query.offset(offset).limit(limit).all()


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(
        Product.id == product_id, Product.deleted == False  # noqa: E712
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/{product_id}/reviews", response_model=list[ReviewOut])
def list_reviews(product_id: int, db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.product_id == product_id).all()


@router.post("/{product_id}/reviews", response_model=ReviewOut, status_code=201)
def add_review(
    product_id: int,
    payload: ReviewIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    review = Review(product_id=product_id, user_id=current_user.id, text=payload.text)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review
