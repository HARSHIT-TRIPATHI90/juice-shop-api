from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ---- Auth ----
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    security_answer: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    email: str
    role: str
    wallet_balance: float

    class Config:
        from_attributes = True


# ---- Products ----
class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image: str

    class Config:
        from_attributes = True


# ---- Basket ----
class BasketItemIn(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1)


class BasketItemOut(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True


class BasketOut(BaseModel):
    id: int
    items: list[BasketItemOut]
    total: float


# ---- Orders ----
class OrderOut(BaseModel):
    id: int
    order_ref: str
    total_price: float
    created_at: datetime

    class Config:
        from_attributes = True


# ---- Address ----
class AddressIn(BaseModel):
    full_name: str
    mobile_num: str
    zip_code: str
    street_address: str
    city: str
    state: str
    country: str


class AddressOut(AddressIn):
    id: int

    class Config:
        from_attributes = True


# ---- Feedback ----
class FeedbackIn(BaseModel):
    comment: str
    rating: int = Field(ge=1, le=5)


class FeedbackOut(BaseModel):
    id: int
    comment: str
    rating: int

    class Config:
        from_attributes = True


# ---- Review ----
class ReviewIn(BaseModel):
    text: str


class ReviewOut(BaseModel):
    id: int
    product_id: int
    text: str

    class Config:
        from_attributes = True


# ---- Complaint ----
class ComplaintIn(BaseModel):
    message: str
