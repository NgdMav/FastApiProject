from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Post(Base):
    __tablename__ = "posts"
    # __table_args__ = {"schema": "fastapi"}

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='True')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    # owner_id = Column(Integer, ForeignKey("fastapi.users.id", ondelete="CASCADE"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    # __table_args__ = {"schema": "fastapi"}

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

class Vote(Base):
    __tablename__ = "votes"
    # __table_args__ = {"schema": "fastapi"}

    # post_id = Column(Integer, ForeignKey("fastapi.posts.id", ondelete="CASCADE"), primary_key=True)
    # user_id = Column(Integer, ForeignKey("fastapi.users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)