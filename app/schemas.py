from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CurrentUser(UserBase):
    id: int
    created_at: datetime

# class UserLogin(BaseModel):
#     username: str
#     password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    # owner_id: int
    owner: UserResponse

    class Config:
        from_attributes = True

class PostResponse(BaseModel):
    Post: Post
    votes: int

class Vote(BaseModel):
    post_id: int
    dir: int