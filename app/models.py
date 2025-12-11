from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.database import Base

class Post(Base):
    __tablename__ = "posts"
    __table_args__ = {"schema": "fastapi"}

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='True')
    created_at = Column(DateTime, nullable=False, server_default=func.now())