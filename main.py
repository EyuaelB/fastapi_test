from fastapi import FastAPI
from routes import auth, posts
from database import init_db

app = FastAPI()

init_db()

app.include_router(auth.router)
app.include_router(posts.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application"}
