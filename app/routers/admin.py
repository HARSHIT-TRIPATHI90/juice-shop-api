from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.security import require_admin
from ..models.db_models import User, Order, Product
from ..models.schemas import UserOut, OrderOut, ProductOut

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/users", response_model=list[UserOut])
def list_all_users(db: Session = Depends(get_db), _admin: User = Depends(require_admin)):
    return db.query(User).all()


@router.get("/orders", response_model=list[OrderOut])
def list_all_orders(db: Session = Depends(get_db), _admin: User = Depends(require_admin)):
    return db.query(Order).all()


@router.get("/products", response_model=list[ProductOut])
def list_all_products(db: Session = Depends(get_db), _admin: User = Depends(require_admin)):
    # Includes soft-deleted products, unlike the public endpoint.
    return db.query(Product).all()
