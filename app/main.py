from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from app import models
from app.database import engine
from app.routers import post, user

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

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

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(post.router)
app.include_router(user.router)