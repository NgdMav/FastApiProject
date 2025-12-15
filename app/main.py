from fastapi import FastAPI
from fastapi.middleware import cors

from app import models
from app.config import settings
from app.database import engine
from app.routers import post, user, auth, vote

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000"
]
app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)