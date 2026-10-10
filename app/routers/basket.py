from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.security import get_current_user
from ..models.db_models import User, Basket, BasketItem, Product
from ..models.schemas import BasketItemIn, BasketOut, BasketItemOut

router = APIRouter(prefix="/api/basket", tags=["basket"])


def _get_or_create_basket(db: Session, user: User) -> Basket:
    basket = db.query(Basket).filter(Basket.user_id == user.id).first()
    if not basket:
        basket = Basket(user_id=user.id)
        db.add(basket)
        db.commit()
        db.refresh(basket)
    return basket


def _serialize(basket: Basket) -> BasketOut:
    items = []
    total = 0.0
    for item in basket.items:
        if item.product and not item.product.deleted:
            items.append(BasketItemOut(
                id=item.id,
                product_id=item.product_id,
                product_name=item.product.name,
                quantity=item.quantity,
                unit_price=item.product.price,
            ))
            total += item.product.price * item.quantity
    return BasketOut(id=basket.id, items=items, total=round(total, 2))


@router.get("", response_model=BasketOut)
def get_my_basket(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    basket = _get_or_create_basket(db, current_user)
    return _serialize(basket)


@router.post("/items", response_model=BasketOut, status_code=201)
def add_item(
    payload: BasketItemIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = db.query(Product).filter(
        Product.id == payload.product_id, Product.deleted == False  # noqa: E712
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    basket = _get_or_create_basket(db, current_user)
    existing = next((i for i in basket.items if i.product_id == payload.product_id), None)
    if existing:
        existing.quantity += payload.quantity
    else:
        db.add(BasketItem(basket_id=basket.id, product_id=payload.product_id, quantity=payload.quantity))
    db.commit()
    db.refresh(basket)
    return _serialize(basket)


@router.delete("/items/{item_id}", response_model=BasketOut)
def remove_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    basket = _get_or_create_basket(db, current_user)
    item = db.query(BasketItem).filter(
        BasketItem.id == item_id, BasketItem.basket_id == basket.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in your basket")
    db.delete(item)
    db.commit()
    db.refresh(basket)
    return _serialize(basket)
