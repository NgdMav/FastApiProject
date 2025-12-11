from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "Title of post 1", "content": "Content of post 1", "id": 1},
            {"title": "Title of post 2", "content": "Content of post 2", "id": 2},]

def find_post(post_id: int):
    for post in my_posts:
        if post["id"] == post_id:
            return post
    return None

def find_index_post(post_id: int):
    for index, post in enumerate(my_posts):
        if post["id"] == post_id:
            return index
    return None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data":my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{post_id}")
def get_post(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "Post not found"}
    return {"data": post}

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    index = find_index_post(post_id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{post_id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(post_id: int, post: Post):
    index = find_index_post(post_id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    post_dict = post.model_dump()
    post_dict["id"] = post_id
    my_posts[index] = post_dict
    return {"data": post_dict}