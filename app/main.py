import time
from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

try:
    conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres",
                            port="5432", cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connected successfully")
except Exception as error:
    print("Connection failed")
    print("Error: ", error)
finally:
    pass

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
    cursor.execute("SELECT * FROM fastapi.fastapi.posts;")
    posts = cursor.fetchall()
    return {"data":posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO fastapi.fastapi.posts (title, content, published)
                      VALUES (%s, %s, %s) returning *;""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{post_id}")
def get_post(post_id: int):
    cursor.execute("""SELECT * FROM fastapi.fastapi.posts WHERE id = %s;""",
                   (str(post_id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found")

    return {"data": post}

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    cursor.execute("""DELETE FROM fastapi.fastapi.posts WHERE id = %s returning *;""",
                   (str(post_id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{post_id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(post_id: int, post: Post):
    cursor.execute("""UPDATE fastapi.fastapi.posts SET title = %s, content = %s,
                                                       published = %s where id = %s
                      returning *;""",
                   (post.title, post.content, post.published, post_id))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found")
    return {"data": updated_post}