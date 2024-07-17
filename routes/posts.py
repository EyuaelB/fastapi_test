from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from schemas import PostCreate, PostResponse
from services.post__service import create_post, get_user_posts, delete_post
from dependencies import get_db, verify_token
from models import User

router = APIRouter()

@router.post(
    "/posts",
    response_model=PostResponse,
    summary="Create a new post",
    description="Create a post by providing the post content."
)
def add_post(post: PostCreate, token: str = Depends(verify_token), db: Session = Depends(get_db)):
    user_id = db.query(User).filter(User.email == token).first().id
    db_post = create_post(db=db, post=post, user_id=user_id)
    return db_post

@router.get(
    "/posts",
    response_model=List[PostResponse],
    summary="Retrieve user posts",
    description="Get all posts created by the authenticated user."
)
def get_posts(token: str = Depends(verify_token), db: Session = Depends(get_db)):
    user_id = db.query(User).filter(User.email == token).first().id
    posts = get_user_posts(db=db, user_id=user_id)
    return posts

@router.delete(
    "/posts/{post_id}",
    summary="Delete a post",
    description="Delete a post by its ID for the authenticated user."
)
def delete_post(post_id: int, token: str = Depends(verify_token), db: Session = Depends(get_db)):
    user_id = db.query(User).filter(User.email == token).first().id
    success = delete_post(db=db, post_id=post_id, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"detail": "Post deleted successfully"}
