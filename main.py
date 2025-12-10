from typing import Optional

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data":"Your posts"}

@app.post("/createposts")
def create_posts(new_post: Post):
    print(new_post)
    return {"data": new_post.model_dump()}