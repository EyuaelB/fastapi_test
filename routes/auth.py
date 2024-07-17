from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import UserCreate, Token
from services.auth_service import create_user, authenticate_user, create_access_token, create_refresh_token
from dependencies import get_db
from models import User
from services.auth_service import verify_token

router = APIRouter()

@router.post(
    "/signup",
    response_model=Token,
    summary="Sign up a new user",
    description="Create a new user account by providing an email and password."
)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = create_user(db=db, user=user)
    access_token = create_access_token(email=new_user.email)
    refresh_token = create_refresh_token(email=new_user.email)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post(
    "/login",
    response_model=Token,
    summary="Log in a user",
    description="Authenticate a user and return access and refresh tokens."
)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(email=db_user.email)
    refresh_token = create_refresh_token(email=db_user.email)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post(
    "/token/refresh",
    response_model=Token,
    summary="Refresh access token",
    description="Generate a new access token using a valid refresh token."
)
def refresh_token(refresh_token: str):
    email = verify_token(refresh_token, is_refresh=True)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    access_token = create_access_token(email=email)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
