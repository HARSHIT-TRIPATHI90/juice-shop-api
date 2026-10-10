from sqlalchemy import (
    Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..core.database import Base


def now():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="customer", nullable=False)  # customer | admin | deluxe
    wallet_balance = Column(Float, default=0.0)
    security_answer_hash = Column(String, nullable=True)
    created_at = Column(DateTime, default=now)

    addresses = relationship("Address", back_populates="owner", cascade="all, delete-orphan")
    cards = relationship("Card", back_populates="owner", cascade="all, delete-orphan")
    basket = relationship("Basket", back_populates="owner", uselist=False, cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="owner", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="author", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="author", cascade="all, delete-orphan")
    complaints = relationship("Complaint", back_populates="author", cascade="all, delete-orphan")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, default="")
    price = Column(Float, nullable=False)
    image = Column(String, default="undefined.jpg")
    deleted = Column(Boolean, default=False)

    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    full_name = Column(String)
    mobile_num = Column(String)
    zip_code = Column(String)
    street_address = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)

    owner = relationship("User", back_populates="addresses")


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    full_name = Column(String)
    card_num_last4 = Column(String)   # only last 4 digits stored
    exp_month = Column(Integer)
    exp_year = Column(Integer)

    owner = relationship("User", back_populates="cards")


class Basket(Base):
    __tablename__ = "baskets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    owner = relationship("User", back_populates="basket")
    items = relationship("BasketItem", back_populates="basket", cascade="all, delete-orphan")


class BasketItem(Base):
    __tablename__ = "basket_items"

    id = Column(Integer, primary_key=True, index=True)
    basket_id = Column(Integer, ForeignKey("baskets.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)

    basket = relationship("Basket", back_populates="items")
    product = relationship("Product")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_ref = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_price = Column(Float, nullable=False)
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=True)
    created_at = Column(DateTime, default=now)

    owner = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    price_at_purchase = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    comment = Column(Text)
    rating = Column(Integer)
    created_at = Column(DateTime, default=now)

    author = relationship("User", back_populates="feedbacks")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    text = Column(Text)
    created_at = Column(DateTime, default=now)

    product = relationship("Product", back_populates="reviews")
    author = relationship("User", back_populates="reviews")


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text)
    file_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=now)

    author = relationship("User", back_populates="complaints")
