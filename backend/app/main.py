from fastapi import FastAPI
from posts.router import router as post_router
from seed import router as seed_router 
from contextlib import asynccontextmanager
from database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()    
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(post_router)
app.include_router(seed_router)

@app.get("/", tags=["Home"])
async def root():
    return {"message": "Hello, World!"}
