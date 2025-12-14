from fastapi import FastAPI
from app import models
from app.config import settings
from app.database import engine
from app.routers import post, user, auth, vote

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)