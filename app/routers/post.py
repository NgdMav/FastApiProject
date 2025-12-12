from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM fastapi.fastapi.posts;")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO fastapi.fastapi.posts (title, content, published)
    #                   VALUES (%s, %s, %s) returning *;""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM fastapi.fastapi.posts WHERE id = %s;""",
    #                (str(post_id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found")

    return post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM fastapi.fastapi.posts WHERE id = %s returning *;""",
    #                (str(post_id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == post_id)
    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found")
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{post_id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostResponse)
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE fastapi.fastapi.posts SET title = %s, content = %s,
    #                                                    published = %s where id = %s
    #                   returning *;""",
    #                (post.title, post.content, post.published, post_id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == post_id)
    if updated_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found")
    updated_post.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return updated_post.first()