from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from schemas import PostCreate, PostResponse
from typing import List
from models import User
from services.post__service import create_post, get_user_posts, delete_post
from models import User
from dependencies import get_db, verify_token

router = APIRouter()

@router.post("/posts", response_model=PostResponse)
def add_post(post: PostCreate, token: str = Depends(verify_token), db: Session = Depends(get_db)):
    user_id = db.query(User).filter(User.email == token).first().id
    db_post = create_post(db=db, post=post, user_id=user_id)
    return db_post

@router.get("/posts", response_model=List[PostResponse])
def get_posts(token: str = Depends(verify_token), db: Session = Depends(get_db)):
    user_id = db.query(User).filter(User.email == token).first().id
    posts = get_user_posts(db=db, user_id=user_id)
    return posts

@router.delete("/posts/{post_id}")
def delete_post(post_id: int, token: str = Depends(verify_token), db: Session = Depends(get_db)):
    user_id = db.query(User).filter(User.email == token).first().id
    success = delete_post(db=db, post_id=post_id, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"detail": "Post deleted successfully"}
