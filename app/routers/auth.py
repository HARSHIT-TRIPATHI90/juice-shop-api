from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordRequestForm
from ..core.database import get_db
from ..core.security import hash_password, verify_password, create_access_token, get_current_user
from ..models.db_models import User, Basket
from ..models.schemas import RegisterRequest, LoginRequest, TokenResponse, UserOut

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role="customer",
        security_answer_hash=hash_password(payload.security_answer) if payload.security_answer else None,
    )
    db.add(user)
    try:
        db.flush()
        db.add(Basket(user_id=user.id))
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    # Same error for "no such user" and "wrong password" to avoid
    # user-enumeration via response differences.
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return TokenResponse(access_token=token)

@router.post("/token")
def token(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": access, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user
