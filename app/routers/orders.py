import secrets
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.security import get_current_user
from ..models.db_models import User, Basket, Order, OrderItem, Address
from ..models.schemas import OrderOut

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post("", response_model=OrderOut, status_code=201)
def checkout(
    address_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    basket = db.query(Basket).filter(Basket.user_id == current_user.id).first()
    if not basket or not basket.items:
        raise HTTPException(status_code=400, detail="Basket is empty")

    if address_id is not None:
        address = db.query(Address).filter(
            Address.id == address_id, Address.user_id == current_user.id
        ).first()
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")

    total = 0.0
    order = Order(
        order_ref=secrets.token_hex(8),
        user_id=current_user.id,
        total_price=0,
        address_id=address_id,
    )
    db.add(order)
    db.flush()

    for item in basket.items:
        if not item.product or item.product.deleted:
            continue
        price = item.product.price
        total += price * item.quantity
        db.add(OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_purchase=price,
        ))

    order.total_price = round(total, 2)
    for item in list(basket.items):
        db.delete(item)
    db.commit()
    db.refresh(order)
    return order


@router.get("", response_model=list[OrderOut])
def list_my_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Order).filter(Order.user_id == current_user.id).all()


@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = db.query(Order).filter(
        Order.id == order_id, Order.user_id == current_user.id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
