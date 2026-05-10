from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserCreate, Token, LoginRequest, UserOut
from app.core.security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(401, "Неверные учетные данные")
    return {"access_token": create_access_token({"sub": str(user.id)}), "token_type": "bearer"}

@router.post("/register", response_model=UserOut, status_code=201)
def register(req: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == req.email).first():
        raise HTTPException(400, "Email уже зарегистрирован")
    user = User(email=req.email, hashed_password=get_password_hash(req.password), role=req.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user