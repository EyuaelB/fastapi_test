from pydantic import BaseModel, EmailStr, constr, Field
from typing import List, Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=6)

class UserResponse(BaseModel):
    id: int
    email: EmailStr

class PostCreate(BaseModel):
    text: constr(max_length=1048576)  # Limit to 1 MB

class PostResponse(BaseModel):
    id: int
    text: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
