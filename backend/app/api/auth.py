from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.databse import get_db
from backend.app.schemas.user import UserCreate, UserLogin, UserOut
from backend.app.models.user import User
from backend.app.core.security import hash_password, verify_password, create_access_token



router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code = 400, detail = "Username already exists")
    db_user = User (
        username = user.username,
        email = user.email,
        hashed_password = hash_password(user.password)
    )
    db.add(db_user)
    db.comimit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code = 401, detail="Invalid credentials")
    toekn = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}